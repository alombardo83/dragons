from django.contrib import admin
from django.utils.translation import gettext as _
from .models import Season, Team, Match

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name','active')
    search_fields = ['name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','active')
    search_fields = ['name']
    list_filter = ('active',)
    ordering = ('name',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('get_team1_name', 'get_team2_name', 'date_time', 'played', 'get_score')
    search_fields = ['get_team1_name', 'get_team2_name']
    list_filter = ('season__name', 'round')
    ordering = ('season__name', 'round', 'date_time')
    fieldsets = (
        (None, {
            'fields': ('season', 'round', 'date_time', 'played', ('team1', 'team2'), ('drops1', 'drops2'), ('penalties1', 'penalties2'), ('tries1', 'tries2'), ('conversions1', 'conversions2'), ('withdrawn_team1', 'withdrawn_team2')),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'withdrawn_team1' in form.changed_data:
            if obj.withdrawn_team1:
            	obj.team1.penalty_points += 2
            else:
            	obj.team1.penalty_points -= 2
        
        if 'withdrawn_team2' in form.changed_data:
            if obj.withdrawn_team2:
            	obj.team2.penalty_points += 2
            else:
            	obj.team2.penalty_points -= 2
        super().save_model(request, obj, form, change)

    def get_team1_name(self, obj):
        return obj.team1.name
    get_team1_name.short_description = 'Nom équipe domicile'

    def get_team2_name(self, obj):
        return obj.team2.name
    get_team2_name.short_description = 'Nom équipe extérieur'
    
    def get_score(self, obj):
        return '{} - {}'.format(obj.score_team1, obj.score_team2)
    get_score.short_description = 'Score'
