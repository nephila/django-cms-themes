VERSION = (1,0,8)
__version__ = "1.0.8"
import random
import os
import sys

def init_themes():
    if not hasattr(settings, 'THEMES_DIR'):
        if hasattr(settings, 'PROJECT_DIR'):
            THEMES_DIR = os.path.join(settings.PROJECT_DIR, 'themes')
        if hasattr(settings, 'PROJECT_HOME'):
            THEMES_DIR = os.path.join(settings.PROJECT_HOME, 'themes')
        if not os.path.exists(THEMES_DIR):
            os.makedirs(THEMES_DIR)
        settings.STATICFILES_DIRS = (
            ('themes', os.path.join(settings.PROJECT_DIR, "themes")),
        ) + settings.STATICFILES_DIRS
        setattr(settings, 'THEMES_DIR', THEMES_DIR)
    if not hasattr(settings, 'DEFAULT_CMS_TEMPLATES'):
        setattr(settings, 'DEFAULT_CMS_TEMPLATES', settings.CMS_TEMPLATES)
    if settings.THEMES_DIR not in settings.TEMPLATE_DIRS:
        settings.TEMPLATE_DIRS = list(settings.TEMPLATE_DIRS) + [settings.THEMES_DIR,]
    if not hasattr(settings, 'DEFAULT_TEMPLATE_DIRS'):
        setattr(settings, 'DEFAULT_TEMPLATE_DIRS', settings.TEMPLATE_DIRS)
    if not hasattr(settings, 'DEFAULT_STATICFILES_DIRS'):
        setattr(settings, 'DEFAULT_STATICFILES_DIRS', settings.STATICFILES_DIRS)

def set_themes():
    if len(sys.argv)>1:
        raise RuntimeError("Running from command line is unsupported")
    try:
        if not Site.objects.filter(id=settings.SITE_ID):
            return False
        site = Site.objects.get(id=settings.SITE_ID)
    except:
        return False

    themes = None

    if hasattr(site, 'theme_set'):
        print list(settings)
        try:
            themes = [theme.name for theme in site.theme_set.all()]

            if not themes:
                return False

            theme_templates = []
            theme_static = []
            for theme_dir in os.listdir(settings.THEMES_DIR):
                if theme_dir in themes:
                    theme_full_path = os.path.join(settings.THEMES_DIR, theme_dir)
                    if os.path.isdir(theme_full_path) and 'templates' in os.listdir(theme_full_path):
                        template_path = os.path.join(theme_full_path, 'templates')
                        setattr(settings, 'TEMPLATE_DIRS', (template_path,) + settings.DEFAULT_TEMPLATE_DIRS)
                        for template in os.listdir(template_path):
                            template_display = '%s (%s)' % (template.replace('_', ' ').title().split('.')[0], theme_dir)
                            theme_templates.append((template, template_display))

            setattr(settings, 'CMS_TEMPLATES', list(theme_templates) + list(settings.DEFAULT_CMS_TEMPLATES))
            setattr(settings, 'STATICFILES_DIRS', [settings.THEMES_DIR] + list(settings.DEFAULT_STATICFILES_DIRS))
        except:
            return False

try:
    import django
    from django.conf import settings
    from django.contrib.sites.models import Site
    from cms.conf.patch import post_patch
    from cms_themes.models import Theme

    init_themes()
    set_themes()
except Exception as ex:
    print 'An error occured setting up the themes: %s' % ex
