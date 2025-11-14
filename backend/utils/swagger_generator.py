import inspect
import re
from typing import Dict, List, Any, Optional
from flask import Blueprint, current_app, Flask


class SwaggerGenerator:
    def __init__(self):
        self.spec = {
            "swagger": "2.0",
            "info": {
                "title": "API Documentation",
                "description": "Автоматически сгенерированная документация API",
                "version": "1.0.0"
            },
            "basePath": "/",
            "schemes": ["http"],
            "paths": {},
            "definitions": {}
        }
    
    def parse_docstring(self, func) -> Dict[str, Any]:
        """Парсит docstring функции для извлечения информации о API"""
        docstring = inspect.getdoc(func)
        if not docstring:
            return {
                "summary": func.__name__.replace('_', ' ').title(),
                "description": "",
                "parameters": [],
                "responses": {
                    "200": {
                        "description": "Success",
                        "schema": {"type": "object"}
                    }
                }
            }
        
        lines = docstring.strip().split('\n')
        summary = lines[0] if lines else func.__name__.replace('_', ' ').title()
        description = []
        parameters = []
        responses = {}
        
        current_section = None
        
        for line in lines[1:]:
            line = line.strip()
            
            # Парсинг параметров
            if line.startswith('Args:'):
                current_section = 'args'
                continue
            elif line.startswith('Returns:'):
                current_section = 'returns'
                continue
            elif line.startswith('Responses:'):
                current_section = 'responses'
                continue
            
            if current_section == 'args' and line:
                # Парсинг параметров в формате: name (type): description
                param_match = re.match(r'(\w+)\s*\(([^)]+)\):\s*(.+)', line)
                if param_match:
                    param_name, param_type, param_desc = param_match.groups()
                    parameters.append({
                        "name": param_name,
                        "in": "query" if param_type.lower() in ['str', 'int', 'bool', 'float'] else "body",
                        "type": self._map_python_type_to_swagger(param_type),
                        "required": True,
                        "description": param_desc
                    })
            elif current_section == 'returns' and line:
                description.append(line)
            elif current_section == 'description' and line:
                description.append(line)
            elif not line.startswith(('Args:', 'Returns:', 'Responses:')) and current_section != 'args':
                description.append(line)
        
        # Дефолтные ответы
        if not responses:
            responses = {
                "200": {
                    "description": "Success",
                    "schema": {"type": "object"}
                }
            }
        
        return {
            "summary": summary,
            "description": '\n'.join(description).strip(),
            "parameters": parameters,
            "responses": responses
        }
    
    def _map_python_type_to_swagger(self, py_type: str) -> str:
        """Маппинг Python типов в Swagger типы"""
        type_mapping = {
            'str': 'string',
            'int': 'integer',
            'float': 'number',
            'bool': 'boolean',
            'list': 'array',
            'dict': 'object'
        }
        return type_mapping.get(py_type.lower(), 'string')
    
    def extract_http_method(self, rule) -> str:
        """Извлекает HTTP метод из правила"""
        methods = [method for method in rule.methods if method not in ['HEAD', 'OPTIONS']]
        return methods[0].lower() if methods else 'get'
    
    def generate_spec_for_blueprint(self, blueprint: Blueprint) -> Dict[str, Any]:
        """Генерирует Swagger спецификацию для blueprint"""
        paths = {}
        
        if not current_app:
            return paths
            
        for rule in current_app.url_map.iter_rules():
            if rule.endpoint.startswith(blueprint.name + '.'):
                view_func = current_app.view_functions.get(rule.endpoint)
                if view_func:
                    path = str(rule.rule)
                    method = self.extract_http_method(rule)
                    
                    # Получаем информацию из docstring
                    doc_info = self.parse_docstring(view_func)
                    
                    if path not in paths:
                        paths[path] = {}
                    
                    paths[path][method] = {
                        "summary": doc_info["summary"],
                        "description": doc_info["description"],
                        "parameters": doc_info["parameters"],
                        "responses": doc_info["responses"]
                    }
        
        return paths
    
    def generate_full_spec(self, app: Flask = None) -> Dict[str, Any]:
        all_paths = {}
        
        # Используем переданный app или current_app
        flask_app = app or current_app
        
        if not flask_app:
            return self.spec
        
        # Получаем все зарегистрированные blueprints
        for blueprint_name, blueprint in flask_app.blueprints.items():
            blueprint_paths = self.generate_spec_for_blueprint(blueprint)
            all_paths.update(blueprint_paths)
        
        self.spec["paths"] = all_paths
        return self.spec


def auto_swagger(blueprint: Blueprint):
    def decorator(func):
        return func
    return decorator


def create_swagger_spec(app=None):
    generator = SwaggerGenerator()
    return generator.generate_full_spec(app)