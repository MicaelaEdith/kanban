LANGUAGES = ["en", "es", "it", "pt", "fr"]

LANGUAGE_NAMES = {
    "en": "English",
    "es": "Español",
    "it": "Italiano",
    "pt": "Português",
    "fr": "Français",
}

TRANSLATIONS = {
    "en": {
        "window_title": "Kanban Board",
        "boards": "Boards",
        "create": "Create",
        "delete": "Delete",
        "back": "\u2190 Back",
        "add": "Add",
        "rename": "Rename",
        "column_todo": "To do",
        "column_progress": "In progress",
        "column_done": "Done",
        "task_count_singular": "{count} task",
        "task_count_plural": "{count} tasks",
        "project_name_placeholder": "New project name...",
        "task_placeholder": "New task...",
        "no_projects": "No projects. Create one above.",
        "delete_project_title": "Delete project",
        "delete_project_msg": 'Delete project "{name}"?',
        "rename_project_title": "Rename project",
        "rename_project_label": "New name:",
    },
    "es": {
        "window_title": "Tablero Kanban",
        "boards": "Tableros",
        "create": "Crear",
        "delete": "Eliminar",
        "back": "\u2190 Volver",
        "add": "Agregar",
        "rename": "Renombrar",
        "column_todo": "Por hacer",
        "column_progress": "En progreso",
        "column_done": "Hecho",
        "task_count_singular": "{count} tarea",
        "task_count_plural": "{count} tareas",
        "project_name_placeholder": "Nombre del nuevo proyecto...",
        "task_placeholder": "Nueva tarea...",
        "no_projects": "No hay proyectos. Creá uno arriba.",
        "delete_project_title": "Eliminar proyecto",
        "delete_project_msg": '¿Eliminar el proyecto "{name}"?',
        "rename_project_title": "Renombrar proyecto",
        "rename_project_label": "Nuevo nombre:",
    },
    "it": {
        "window_title": "Kanban Board",
        "boards": "Lavagne",
        "create": "Crea",
        "delete": "Elimina",
        "back": "\u2190 Indietro",
        "add": "Aggiungi",
        "rename": "Rinomina",
        "column_todo": "Da fare",
        "column_progress": "In corso",
        "column_done": "Fatto",
        "task_count_singular": "{count} attivit\u00e0",
        "task_count_plural": "{count} attivit\u00e0",
        "project_name_placeholder": "Nome nuovo progetto...",
        "task_placeholder": "Nuova attivit\u00e0...",
        "no_projects": "Nessun progetto. Creane uno sopra.",
        "delete_project_title": "Elimina progetto",
        "delete_project_msg": 'Eliminare il progetto "{name}"?',
        "rename_project_title": "Rinomina progetto",
        "rename_project_label": "Nuovo nome:",
    },
    "pt": {
        "window_title": "Quadro Kanban",
        "boards": "Quadros",
        "create": "Criar",
        "delete": "Eliminar",
        "back": "\u2190 Voltar",
        "add": "Adicionar",
        "rename": "Renomear",
        "column_todo": "A fazer",
        "column_progress": "Em andamento",
        "column_done": "Conclu\u00eddo",
        "task_count_singular": "{count} tarefa",
        "task_count_plural": "{count} tarefas",
        "project_name_placeholder": "Nome do novo projeto...",
        "task_placeholder": "Nova tarefa...",
        "no_projects": "Nenhum projeto. Crie um acima.",
        "delete_project_title": "Excluir projeto",
        'delete_project_msg': 'Excluir projeto "{name}"?',
        "rename_project_title": "Renomear projeto",
        "rename_project_label": "Novo nome:",
    },
    "fr": {
        "window_title": "Tableau Kanban",
        "boards": "Tableaux",
        "create": "Cr\u00e9er",
        "delete": "Supprimer",
        "back": "\u2190 Retour",
        "add": "Ajouter",
        "rename": "Renommer",
        "column_todo": "\u00c0 faire",
        "column_progress": "En cours",
        "column_done": "Termin\u00e9",
        "task_count_singular": "{count} t\u00e2che",
        "task_count_plural": "{count} t\u00e2ches",
        "project_name_placeholder": "Nom du nouveau projet...",
        "task_placeholder": "Nouvelle t\u00e2che...",
        "no_projects": "Aucun projet. Cr\u00e9ez-en un ci-dessus.",
        "delete_project_title": "Supprimer le projet",
        'delete_project_msg': 'Supprimer le projet "{name}" ?',
        "rename_project_title": "Renommer le projet",
        "rename_project_label": "Nouveau nom :",
    },
}

_current_language = "en"


def set_language(lang):
    global _current_language
    if lang in TRANSLATIONS:
        _current_language = lang


def get_language():
    return _current_language


def t(key, **kwargs):
    text = TRANSLATIONS.get(_current_language, TRANSLATIONS["en"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text
