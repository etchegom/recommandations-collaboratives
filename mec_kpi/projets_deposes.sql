SELECT "projects_project"."id",
    "projects_project"."submitted_by_id",
    "projects_project"."status",
    "projects_project"."ro_key",
    "projects_project"."last_name",
    "projects_project"."first_name",
    "projects_project"."publish_to_cartofriches",
    "projects_project"."exclude_stats",
    "projects_project"."inactive_since",
    "projects_project"."inactive_reason",
    "projects_project"."last_members_activity_at",
    "projects_project"."muted",
    "projects_project"."org_name",
    "projects_project"."created_on",
    "projects_project"."updated_on",
    "projects_project"."name",
    "projects_project"."phone",
    "projects_project"."description",
    "projects_project"."advisors_note",
    "projects_project"."advisors_note_on",
    "projects_project"."advisors_note_by_id",
    "projects_project"."location",
    "projects_project"."location_x",
    "projects_project"."location_y",
    "projects_project"."commune_id",
    "projects_project"."impediments",
    "projects_project"."deleted"
FROM "projects_project"
    INNER JOIN "projects_project_sites" ON (
        "projects_project"."id" = "projects_project_sites"."project_id"
    )
WHERE (
        "projects_project"."deleted" IS NULL
        AND "projects_project_sites"."site_id" = %s
        AND ("projects_project"."created_on" AT TIME ZONE %s)::date >= %s
    );
-- (6, 'Europe/Paris', datetime.date(2024, 4, 6))
