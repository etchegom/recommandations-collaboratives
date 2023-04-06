# encoding: utf-8

"""
Tests for project application

authors: raphael.marvie@beta.gouv.fr, guillaume.libersat@beta.gouv.fr
created: 2021-06-01 10:11:56 CEST
"""


import pytest
from actstream.models import action_object_stream
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from model_bakery import baker
from model_bakery.recipe import Recipe
from pytest_django.asserts import assertContains
from urbanvitaliz.utils import login

from .. import models

########################################################################
# notes
########################################################################


# Public conversation
@pytest.mark.django_db
def test_create_conversation_message_not_available_for_non_logged_users(
    request, client
):
    project = Recipe(models.Project, sites=[get_current_site(request)]).make()
    url = reverse("projects-conversation-create-message", args=[project.id])
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_conversation_message_not_available_for_outsiders(request, client):
    with login(client):
        project = Recipe(models.Project, sites=[get_current_site(request)]).make()
        url = reverse("projects-conversation-create-message", args=[project.id])
        response = client.post(
            url,
            data={"content": "this is some content"},
        )
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_conversation_message_available_for_project_collaborators(
    request, client
):
    membership = baker.make(models.ProjectMember)
    project = Recipe(
        models.Project,
        sites=[get_current_site(request)],
        status="READY",
        projectmember_set=[membership],
    ).make()

    with login(client, user=membership.member):
        url = reverse("projects-conversation-create-message", args=[project.id])
        response = client.post(
            url,
            data={"content": "this is some content"},
        )
    note = models.Note.objects.all()[0]
    assert note.project == project
    assert response.status_code == 302


#
# create


@pytest.mark.django_db
def test_create_note_not_available_for_non_staff_users(request, client):
    project = Recipe(models.Project, sites=[get_current_site(request)]).make()
    url = reverse("projects-create-note", args=[project.id])
    with login(client):
        response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_note_available_for_switchtender(request, client):
    project = Recipe(models.Project, sites=[get_current_site(request)]).make()
    url = reverse("projects-create-note", args=[project.id])
    with login(client, groups=["switchtender"]) as user:
        project.switchtenders_on_site.create(
            switchtender=user, site=get_current_site(request)
        )

        response = client.get(url)
    assert response.status_code == 200
    assertContains(response, 'form id="form-projects-add-note"')


@pytest.mark.django_db
def test_create_private_note_not_available_for_project_collaborator(request, client):
    membership = baker.make(models.ProjectMember)
    project = Recipe(
        models.Project,
        sites=[get_current_site(request)],
        status="READY",
        projectmember_set=[membership],
    ).make()

    with login(client, user=membership.member):
        response = client.post(
            reverse("projects-create-note", args=[project.id]),
            data={"content": "this is some content", "public": False},
        )

    assert response.status_code == 403


# check test exists on conversation
# @pytest.mark.django_db
# def test_switchtender_creates_new_public_note_for_project_and_redirect(request, client):
#     project = Recipe(models.Project, sites=[get_current_site(request)]).make()

#     with login(client, groups=["switchtender"]) as user:
#         project.switchtenders_on_site.create(
#             switchtender=user, site=get_current_site(request)
#         )

#         response = client.post(
#             reverse("projects-create-note", args=[project.id]),
#             data={"content": "this is some content", "public": True},
#         )

#     # note is created
#     note = models.Note.fetch()[0]
#     assert note.project == project
#     assert note.public is True

#     # stream and notifications
#     actions = action_object_stream(note)
#     assert actions.count() == 1
#     assert actions[0].verb == "a envoyé un message"

#     # redirects
#     assert response.status_code == 302


@pytest.mark.django_db
def test_switchtender_creates_new_private_note_for_project_and_redirect(
    request, client
):
    project = Recipe(models.Project, sites=[get_current_site(request)]).make()

    with login(client, groups=["switchtender"]) as user:
        project.switchtenders_on_site.create(
            switchtender=user, site=get_current_site(request)
        )

        response = client.post(
            reverse("projects-create-note", args=[project.id]),
            data={
                "content": "this is some content",
            },
        )

    # note is created
    note = models.Note.fetch()[0]
    assert note.project == project
    assert note.public is False

    # stream and notifications
    actions = action_object_stream(note)
    assert actions.count() == 1
    assert actions[0].verb == "a envoyé un message dans l'espace conseillers"

    # redirects
    assert response.status_code == 302


@pytest.mark.django_db
def test_private_note_hidden_from_project_members(request, client):
    membership = baker.make(models.ProjectMember, member__is_staff=False)
    project = baker.make(
        models.Project,
        sites=[get_current_site(request)],
        status="READY",
        projectmember_set=[membership],
    )

    note = baker.make(models.Note, project=project, content="short note", public=False)

    with login(client, user=membership.member):
        response = client.get(note.get_absolute_url())

    assert response.status_code == 403


@pytest.mark.django_db
def test_public_note_available_to_readers(request, client):
    membership = baker.make(models.ProjectMember)
    project = Recipe(
        models.Project,
        sites=[get_current_site(request)],
        status="READY",
        projectmember_set=[membership],
    ).make()
    note_content = "this is a public note"

    with login(client, groups=["switchtender"]) as user:
        project.switchtenders_on_site.create(
            switchtender=user, site=get_current_site(request)
        )

        response = client.post(
            reverse("projects-conversation-create-message", args=[project.id]),
            data={"content": note_content, "public": True},
        )

    note = models.Note.objects.first()

    with login(client, user=membership.member):
        response = client.get(note.get_absolute_url())

    assertContains(response, note_content)


@pytest.mark.django_db
def test_create_conversation_message_with_attachment_for_project_collaborator(
    request, client
):
    membership = baker.make(models.ProjectMember)
    project = Recipe(
        models.Project,
        sites=[get_current_site(request)],
        status="READY",
        projectmember_set=[membership],
    ).make()

    with login(client, user=membership.member):
        png = SimpleUploadedFile("img.png", b"file_content", content_type="image/png")
        response = client.post(
            reverse("projects-conversation-create-message", args=[project.id]),
            data={
                "content": "this is some content",
                "the_file": png,
            },
        )

    assert response.status_code == 302

    note = models.Note.objects.first()
    assert note
    document = models.Document.on_site.first()
    assert document
    assert document.the_file != ""
    assert document.attached_object == note


#
# update


@pytest.mark.django_db
def test_update_note_not_available_for_non_staff_users(client):
    note = Recipe(models.Note).make()
    url = reverse("projects-update-note", args=[note.id])
    with login(client):
        response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_switchtender_can_update_own_note(request, client):
    with login(client, groups=["switchtender"]) as user:
        note = Recipe(models.Note, created_by=user).make()
        url = reverse("projects-update-note", args=[note.id])

        note.project.switchtenders_on_site.create(
            switchtender=user, site=get_current_site(request)
        )

        response = client.get(url)
    assert response.status_code == 200

    assertContains(response, 'form id="form-projects-update-note"')


@pytest.mark.django_db
def test_switchtender_cant_update_other_switchtender_note(request, client):
    note = Recipe(models.Note).make()
    url = reverse("projects-update-note", args=[note.id])
    with login(client, groups=["switchtender"]) as user:
        note.project.switchtenders_on_site.create(
            switchtender=user, site=get_current_site(request)
        )
        response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_collaborator_can_update_own_public_note(request, client):
    membership = baker.make(models.ProjectMember)
    project = Recipe(
        models.Project,
        sites=[get_current_site(request)],
        projectmember_set=[membership],
    ).make()

    with login(client, user=membership.member) as user:
        note = Recipe(models.Note, created_by=user, project=project, public=True).make()
        response = client.post(
            reverse("projects-update-note", args=[note.id]),
            data={"content": "this is some content"},
        )

    note = models.Note.fetch()[0]
    assert note.project == project
    assert note.public is True
    assert response.status_code == 302


@pytest.mark.django_db
def test_collaborator_cant_update_others_public_note(request, client):
    membership = baker.make(models.ProjectMember)
    project = Recipe(
        models.Project,
        sites=[get_current_site(request)],
        projectmember_set=[membership],
    ).make()

    with login(client, user=membership.member):
        note = Recipe(models.Note, project=project, public=True).make()
        response = client.post(
            reverse("projects-update-note", args=[note.id]),
            data={"content": "this is some content"},
        )

    assert response.status_code == 403


@pytest.mark.django_db
def test_collaborator_cant_update_private_note(request, client):
    membership = baker.make(models.ProjectMember)
    project = Recipe(
        models.Project,
        sites=[get_current_site(request)],
        projectmember_set=[membership],
    ).make()
    with login(client, user=membership.member):
        note = Recipe(models.Note, project=project, public=False).make()
        url = reverse("projects-update-note", args=[note.id])
        response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_note_for_project_and_redirect(request, client):
    project = Recipe(models.Project, sites=[get_current_site(request)]).make()
    note = Recipe(models.Note, project=project).make()
    url = reverse("projects-delete-note", args=[note.id])

    with login(client, groups=["switchtender"]):
        response = client.post(url)

    assert models.Note.objects.count() == 0

    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_note_removes_activity(request, client):
    project = Recipe(models.Project, sites=[get_current_site(request)]).make()

    with login(client, username="addman", groups=["switchtender"]) as user:
        project.switchtenders_on_site.create(
            switchtender=user, site=get_current_site(request)
        )

        client.post(
            reverse("projects-create-note", args=[project.id]),
            data={"content": "content", "public": True},
        )

    note = models.Note.objects.first()
    assert note

    assert action_object_stream(note).count()

    with login(client, username="removeman", groups=["switchtender"]):
        client.post(reverse("projects-delete-note", args=[note.id]))

    assert action_object_stream(note).count() == 0


# eof
