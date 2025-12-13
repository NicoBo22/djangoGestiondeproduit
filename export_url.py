import os
from django.core.wsgi import get_wsgi_application
from django.urls import get_resolver

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestiondejury.settings")
application = get_wsgi_application()

def list_urls(patterns=None, prefix=''):
    if patterns is None:
        patterns = get_resolver().url_patterns

    for p in patterns:
        # include(...)
        if hasattr(p, 'url_patterns'):
            yield from list_urls(p.url_patterns, prefix + str(p.pattern))
        else:
            # URL finale
            yield prefix + str(p.pattern)

def export_urls(output_file="urls.txt"):
    urls = list(list_urls())
    with open(output_file, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")
    print(f"Fichier généré : {output_file}")

if __name__ == "__main__":
    export_urls()
