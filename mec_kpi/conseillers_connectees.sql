SELECT "projects_projectswitchtender"."id",
    "projects_projectswitchtender"."switchtender_id",
    "projects_projectswitchtender"."project_id",
    "projects_projectswitchtender"."is_observer",
    "projects_projectswitchtender"."site_id"
FROM "projects_projectswitchtender"
    INNER JOIN "auth_user" ON (
        "projects_projectswitchtender"."switchtender_id" = "auth_user"."id"
    )
WHERE (
        "projects_projectswitchtender"."site_id" = %s
        AND "projects_projectswitchtender"."site_id" = %s
        AND ("auth_user"."last_login" AT TIME ZONE %s)::date >= %s
    );
-- (1, 6, 'Europe/Paris', datetime.date(2024, 4, 6))
