# encoding: utf-8

"""
Views for projects application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2021-05-26 15:56:20 CEST
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from urbanvitaliz.utils import check_if_switchtender, is_switchtender_or_403


from .. import models, signals
from ..forms import DocumentUploadForm, NoteForm, PublicNoteForm, StaffNoteForm
from ..utils import can_administrate_or_403, can_administrate_project, can_manage_or_403


@login_required
def create_public_note(request, project_id=None):
    """Create a new note for a project"""
    project = get_object_or_404(models.Project, sites=request.site, pk=project_id)
    can_manage_or_403(project, request.user)

    if request.method == "POST":
        form = PublicNoteForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.created_by = request.user
            instance.public = True
            instance.save()

            # Check if we have a file or link
            document_form = DocumentUploadForm(request.POST, request.FILES)
            if document_form.is_valid():
                if document_form.cleaned_data["the_file"]:
                    document = document_form.save(commit=False)
                    document.attached_object = instance
                    document.site = request.site
                    document.uploaded_by = request.user
                    document.project = instance.project

                    document.save()

            signals.note_created.send(
                sender=create_note,
                note=instance,
                project=project,
                user=request.user,
            )

    return redirect(reverse("projects-project-detail-conversations", args=[project_id]))


@login_required
def create_note(request, project_id=None):
    """Create a new note for a project"""
    project = get_object_or_404(models.Project, sites=request.site, pk=project_id)
    can_manage_or_403(project, request.user, allow_draft=True)
    is_advisor = can_administrate_project(project, request.user)

    if request.method == "POST":
        if is_advisor:
            form = StaffNoteForm(request.POST)
        else:
            form = NoteForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.created_by = request.user

            if not is_advisor:
                instance.public = True
            instance.save()

            signals.note_created.send(
                sender=create_note,
                note=instance,
                project=project,
                user=request.user,
            )

            return redirect(
                reverse("projects-project-detail-internal-followup", args=[project_id])
            )
    else:
        if is_advisor:
            form = StaffNoteForm()
        else:
            form = NoteForm()
    return render(request, "projects/project/note_create.html", locals())


@login_required
def update_note(request, note_id=None):
    """Update an existing note for a project"""
    note = get_object_or_404(models.Note, pk=note_id)
    project = note.project  # For template consistency

    can_manage_or_403(project, request.user, allow_draft=True)
    if note.created_by != request.user:
        raise PermissionDenied("Vous ne pouvez éditer que vos propres messages.")

    is_advisor = can_administrate_project(project, request.user)

    if not note.public:
        can_administrate_or_403(project, request.user)

    if request.method == "POST":
        if is_advisor:
            form = StaffNoteForm(request.POST, instance=note)
        else:
            form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updated_on = timezone.now()
            instance.save()
            instance.project.updated_on = instance.updated_on
            instance.project.save()
            if instance.public:
                return redirect(
                    reverse(
                        "projects-project-detail-conversations", args=[note.project_id]
                    )
                )

            return redirect(
                reverse(
                    "projects-project-detail-internal-followup", args=[note.project_id]
                )
            )
    else:
        if is_advisor:
            form = StaffNoteForm(instance=note)
        else:
            form = NoteForm(instance=note)
    return render(request, "projects/project/note_update.html", locals())


@login_required
def delete_note(request, note_id=None):
    """Delete existing note for a project"""
    is_switchtender_or_403(request.user)
    note = get_object_or_404(models.Note, pk=note_id)

    if request.method == "POST":
        note.updated_on = timezone.now()
        note.deleted = timezone.now()
        note.save()
        note.project.updated_on = note.updated_on
        note.project.save()

        if note.public:
            return redirect(
                reverse("projects-project-detail-conversations", args=[note.project_id])
            )

    return redirect(
        reverse("projects-project-detail-internal-followup", args=[note.project_id])
    )
