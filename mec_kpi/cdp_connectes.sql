SELECT "projects_projectmember"."id",
    "projects_projectmember"."member_id",
    "projects_projectmember"."project_id",
    "projects_projectmember"."is_owner"
FROM "projects_projectmember"
    INNER JOIN "auth_user" ON (
        "projects_projectmember"."member_id" = "auth_user"."id"
    )
    INNER JOIN "projects_project" ON (
        "projects_projectmember"."project_id" = "projects_project"."id"
    )
    INNER JOIN "projects_project_sites" ON (
        "projects_project"."id" = "projects_project_sites"."project_id"
    )
WHERE (
        "projects_projectmember"."is_owner"
        AND ("auth_user"."last_login" AT TIME ZONE %s)::date >= %s
        AND "projects_project_sites"."site_id" = %s
    );
-- ('Europe/Paris', datetime.date(2024, 4, 6), 6)
