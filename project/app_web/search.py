from wtforms import SubmitField, SearchField

from project.app_config.database import ModelForm

class SearchForm(ModelForm):
    """
    .. uml:: entities.uml
    """
    searchterm = SearchField()

    submit = SubmitField('Search')
