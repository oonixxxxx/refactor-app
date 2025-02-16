import ast
import astor

def refactor_code(code):
    """
    Рефакторинг кода:
    1. Удаление неиспользуемых импортов.
    2. Удаление неиспользуемых переменных.
    3. Удаление дублирующихся импортов.
    4. Удаление неиспользуемых функций.
    5. Удаление пустых строк и лишних пробелов.
    6. Обработка синтаксических ошибок.
    """
    if not code or not code.strip():
        return "Error: Empty code provided."

    try:
        # Парсим код в AST (Abstract Syntax Tree)
        tree = ast.parse(code)

        # Удаление неиспользуемых импортов
        tree = remove_unused_imports(tree)

        # Удаление неиспользуемых переменных
        tree = remove_unused_variables(tree)

        # Удаление дублирующихся импортов
        tree = remove_duplicate_imports(tree)

        # Удаление неиспользуемых функций
        tree = remove_unused_functions(tree)

        # Удаление пустых строк и лишних пробелов
        refactored_code = astor.to_source(tree)
        refactored_code = clean_code(refactored_code)

        return refactored_code

    except SyntaxError as e:
        return f"Syntax Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def remove_unused_imports(tree):
    """
    Удаляет неиспользуемые импорты.
    """
    used_names = set()

    # Собираем все используемые имена
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    # Удаляем неиспользуемые импорты
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            node.names = [alias for alias in node.names if alias.name in used_names]
        elif isinstance(node, ast.ImportFrom):
            node.names = [alias for alias in node.names if alias.name in used_names]

    return tree

def remove_unused_variables(tree):
    """
    Удаляет неиспользуемые переменные.
    """
    used_names = set()

    # Собираем все используемые имена
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    # Удаляем неиспользуемые переменные
    new_body = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            # Проверяем, используются ли переменные
            used = any(target.id in used_names for target in node.targets if isinstance(target, ast.Name))
            if used:
                new_body.append(node)
        else:
            new_body.append(node)

    tree.body = new_body
    return tree

def remove_duplicate_imports(tree):
    """
    Удаляет дублирующиеся импорты.
    """
    imports_seen = set()
    new_body = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            # Фильтруем дублирующиеся импорты
            new_names = []
            for alias in node.names:
                if alias.name not in imports_seen:
                    new_names.append(alias)
                    imports_seen.add(alias.name)
            if new_names:
                node.names = new_names
                new_body.append(node)
        elif isinstance(node, ast.ImportFrom):
            # Фильтруем дублирующиеся импорты
            new_names = []
            for alias in node.names:
                full_name = f"{node.module}.{alias.name}"
                if full_name not in imports_seen:
                    new_names.append(alias)
                    imports_seen.add(full_name)
            if new_names:
                node.names = new_names
                new_body.append(node)
        else:
            new_body.append(node)

    tree.body = new_body
    return tree

def remove_unused_functions(tree):
    """
    Удаляет неиспользуемые функции.
    """
    used_names = set()

    # Собираем все используемые имена
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            used_names.add(node.func.id)

    # Удаляем неиспользуемые функции
    new_body = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name in used_names:
                new_body.append(node)
        else:
            new_body.append(node)

    tree.body = new_body
    return tree

def clean_code(code):
    """
    Удаляет пустые строки и лишние пробелы.
    """
    lines = code.splitlines()
    cleaned_lines = [line.rstrip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)