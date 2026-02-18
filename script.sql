create table if not exists auth_group
(
    id   int auto_increment
        primary key,
    name varchar(150) not null,
    constraint name
        unique (name)
);

create table if not exists culture_category
(
    id             bigint auto_increment
        primary key,
    name           varchar(100) not null,
    description    longtext     null,
    level          varchar(10)  not null,
    created_at     datetime(6)  not null,
    updated_at     datetime(6)  not null,
    description_en longtext     null,
    name_en        varchar(100) null
);

create table if not exists culture_content
(
    id              bigint auto_increment
        primary key,
    title           varchar(255) not null,
    content         longtext     not null,
    cover_image     varchar(500) null,
    created_at      datetime(6)  not null,
    updated_at      datetime(6)  not null,
    category_id     bigint       not null,
    audio_url       varchar(500) null,
    content_type    varchar(20)  not null,
    difficulty      int          not null,
    duration        int          not null,
    like_count      int          not null,
    video_url       varchar(500) null,
    view_count      int          not null,
    content_en      longtext     null,
    paragraphs      json         null,
    title_en        varchar(255) null,
    description     longtext     null,
    description_en  longtext     null,
    structured_data json         null,
    subtitle        varchar(500) null,
    subtitle_en     varchar(500) null,
    constraint culture_content_category_id_72cee7c7_fk_culture_category_id
        foreign key (category_id) references culture_category (id)
);

create table if not exists django_content_type
(
    id        int auto_increment
        primary key,
    app_label varchar(100) not null,
    model     varchar(100) not null,
    constraint django_content_type_app_label_model_76bd3d3b_uniq
        unique (app_label, model)
);

create table if not exists auth_permission
(
    id              int auto_increment
        primary key,
    name            varchar(255) not null,
    content_type_id int          not null,
    codename        varchar(100) not null,
    constraint auth_permission_content_type_id_codename_01ab375a_uniq
        unique (content_type_id, codename),
    constraint auth_permission_content_type_id_2f476e4b_fk_django_co
        foreign key (content_type_id) references django_content_type (id)
);

create table if not exists auth_group_permissions
(
    id            int auto_increment
        primary key,
    group_id      int not null,
    permission_id int not null,
    constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
        unique (group_id, permission_id),
    constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
        foreign key (permission_id) references auth_permission (id),
    constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
        foreign key (group_id) references auth_group (id)
);

create table if not exists django_migrations
(
    id      int auto_increment
        primary key,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied datetime(6)  not null
);

create table if not exists django_session
(
    session_key  varchar(40) not null
        primary key,
    session_data longtext    not null,
    expire_date  datetime(6) not null
);

-- 索引可能已在其他脚本中创建，为避免重复创建导致 ERROR 1061，这里注释掉原始语句
-- create index django_session_expire_date_a5c62663
--     on django_session (expire_date);

create table if not exists hsk_info_faq
(
    id            bigint auto_increment
        primary key,
    category      varchar(50)  not null,
    question      varchar(500) not null,
    answer        longtext     not null,
    related_links json         null,
    `order`       int          not null,
    view_count    int          not null,
    is_featured   tinyint(1)   not null,
    created_at    datetime(6)  not null,
    updated_at    datetime(6)  not null
);

create table if not exists hsk_info_hsklevel
(
    id                bigint auto_increment
        primary key,
    level             int         not null,
    name              varchar(50) not null,
    description       longtext    not null,
    vocabulary_count  int         not null,
    listening_ability longtext    not null,
    reading_ability   longtext    not null,
    writing_ability   longtext    not null,
    exam_duration     int         not null,
    total_score       int         not null,
    passing_score     int         not null,
    exam_structure    json        not null,
    target_audience   longtext    not null,
    study_hours       int         not null,
    icon              varchar(50) not null,
    color             varchar(20) not null,
    created_at        datetime(6) not null,
    updated_at        datetime(6) not null,
    constraint level
        unique (level)
);

create table if not exists hsk_info_examoutline
(
    id             bigint auto_increment
        primary key,
    section        varchar(50)  not null,
    part_number    int          not null,
    title          varchar(200) not null,
    description    longtext     not null,
    question_count int          not null,
    time_limit     int          not null,
    question_types json         not null,
    scoring_method longtext     not null,
    tips           longtext     not null,
    `order`        int          not null,
    created_at     datetime(6)  not null,
    hsk_level_id   bigint       not null,
    constraint hsk_info_examoutline_hsk_level_id_e55840fb_fk_hsk_info_
        foreign key (hsk_level_id) references hsk_info_hsklevel (id)
);

create table if not exists hsk_info_studyguide
(
    id           bigint auto_increment
        primary key,
    title        varchar(200) not null,
    category     varchar(50)  not null,
    content      longtext     not null,
    tips         json         null,
    resources    json         null,
    `order`      int          not null,
    is_featured  tinyint(1)   not null,
    created_at   datetime(6)  not null,
    updated_at   datetime(6)  not null,
    hsk_level_id bigint       not null,
    constraint hsk_info_studyguide_hsk_level_id_bf00ec10_fk_hsk_info_
        foreign key (hsk_level_id) references hsk_info_hsklevel (id)
);

create table if not exists question_examattempt
(
    id              bigint auto_increment
        primary key,
    start_time      datetime(6)   not null,
    end_time        datetime(6)   null,
    score           decimal(5, 2) not null,
    status          varchar(20)   not null,
    answers         json          not null,
    created_at      datetime(6)   not null,
    updated_at      datetime(6)   not null,
    question_set_id bigint        not null,
    user_id         bigint        not null
);

create table if not exists question_examranking
(
    id              bigint auto_increment
        primary key,
    score           decimal(5, 2) not null,
    time_spent      int           not null,
    `rank`          int           not null,
    created_at      datetime(6)   not null,
    updated_at      datetime(6)   not null,
    exam_attempt_id bigint        not null,
    question_set_id bigint        not null,
    user_id         bigint        not null,
    constraint question_examranking_question_set_id_user_id_unique
        unique (question_set_id, user_id)
);

create index question_examranking_exam_attempt_id_idx
    on question_examranking (exam_attempt_id);

create index question_examranking_user_id_idx
    on question_examranking (user_id);

create table if not exists question_examreport
(
    id                   bigint auto_increment
        primary key,
    total_questions      int           not null,
    correct_count        int           not null,
    accuracy_rate        decimal(5, 2) not null,
    time_spent           int           not null,
    category_performance json          not null,
    weak_points          json          not null,
    suggestions          longtext      not null,
    created_at           datetime(6)   not null,
    exam_attempt_id      bigint        not null,
    constraint exam_attempt_id
        unique (exam_attempt_id)
);

create table if not exists question_material
(
    id                   bigint auto_increment
        primary key,
    title                varchar(200) not null,
    level                int          not null,
    section_type         varchar(20)  not null,
    part_number          int          not null,
    content              longtext     not null,
    audio_url            varchar(500) null,
    audio_duration       int          not null,
    material_group       varchar(100) not null,
    play_times           int          not null,
    question_range_start int          not null,
    question_range_end   int          not null,
    `order`              int          not null,
    is_active            tinyint(1)   not null,
    created_at           datetime(6)  not null,
    updated_at           datetime(6)  not null,
    constraint material_group
        unique (material_group)
);

create table if not exists question_questioncategory
(
    id                 bigint auto_increment
        primary key,
    name               varchar(50) not null,
    description        longtext    not null,
    created_at         datetime(6) not null,
    color              varchar(20) not null,
    icon               varchar(50) not null,
    is_active          tinyint(1)  not null,
    level_range        json        null,
    `order`            int         not null,
    parent_category_id bigint      null,
    updated_at         datetime(6) not null,
    constraint question_questioncat_parent_category_id_c08e9842_fk_question_
        foreign key (parent_category_id) references question_questioncategory (id)
);

create table if not exists question_questionset
(
    id                       bigint auto_increment
        primary key,
    title                    varchar(200) not null,
    description              longtext     not null,
    level                    int          not null,
    time_limit               int          not null,
    question_count           int          not null,
    created_at               datetime(6)  not null,
    updated_at               datetime(6)  not null,
    exam_type                varchar(20)  not null,
    listening_audio_duration int          not null,
    listening_audio_url      varchar(500) null
);

create table if not exists question_question
(
    id              bigint auto_increment
        primary key,
    type            varchar(50)  not null,
    level           int          not null,
    content         longtext     not null,
    options         json         not null,
    answer          longtext     not null,
    created_at      datetime(6)  not null,
    updated_at      datetime(6)  not null,
    explanation     longtext     null,
    category_id     bigint       null,
    question_set_id bigint       null,
    difficulty      int          not null,
    audio_duration  int          not null,
    audio_file      varchar(100) null,
    audio_url       varchar(500) null,
    image_file      varchar(100) null,
    image_url       varchar(500) null,
    matching_pairs  json         null,
    ordering_items  json         null,
    passage         longtext     null,
    passage_title   varchar(200) null,
    points          int          not null,
    sub_questions   json         null,
    tags            json         null,
    time_limit      int          not null,
    audio_group     varchar(100) null,
    material_group  varchar(100) null,
    part_number     int          null,
    question_number int          null,
    section_type    varchar(20)  null,
    option_type     varchar(10)  not null,
    constraint question_question_category_id_48dd39ba_fk_question_
        foreign key (category_id) references question_questioncategory (id),
    constraint question_question_question_set_id_689bf451_fk_question_
        foreign key (question_set_id) references question_questionset (id)
);

create table if not exists university_university
(
    id                     bigint auto_increment
        primary key,
    name                   varchar(255)                  not null,
    region                 varchar(100)                  null,
    ranking                int                           null,
    majors                 json                          null,
    description            longtext                      null,
    address                longtext default (_utf8mb3'') not null,
    campus_image_url       varchar(500)                  not null,
    city                   varchar(100)                  not null,
    created_at             datetime(6)                   null,
    email                  varchar(254)                  not null,
    english_name           varchar(255)                  not null,
    features               longtext default (_utf8mb3'') not null,
    history                longtext default (_utf8mb3'') not null,
    international_students int                           not null,
    language_requirements  longtext default (_utf8mb3'') not null,
    logo_url               varchar(500)                  not null,
    min_hsk_level          int                           not null,
    phone                  varchar(50)                   not null,
    popular_majors         json                          null,
    ranking_national       int                           null,
    ranking_world          int                           null,
    scholarship            longtext default (_utf8mb3'') not null,
    tags                   json                          null,
    total_students         int                           not null,
    tuition_fee            decimal(10, 2)                null,
    updated_at             datetime(6)                   null,
    website                varchar(500)                  not null,
    advantages             json                          null,
    campus_life            json                          null,
    description_en         longtext                      null,
    features_en            longtext                      null,
    history_en             longtext                      null
);

create table if not exists user_user
(
    id                   bigint auto_increment
        primary key,
    password             varchar(128) not null,
    last_login           datetime(6)  null,
    is_superuser         tinyint(1)   not null,
    username             varchar(150) not null,
    first_name           varchar(150) not null,
    last_name            varchar(150) not null,
    email                varchar(254) not null,
    is_staff             tinyint(1)   not null,
    is_active            tinyint(1)   not null,
    date_joined          datetime(6)  not null,
    hsk_level            int          not null,
    avatar               varchar(500) null,
    chinese_name         varchar(50)  not null,
    created_at           datetime(6)  null,
    english_name         varchar(50)  not null,
    nationality          varchar(100) not null,
    phone                varchar(20)  not null,
    total_correct_count  int          not null,
    total_practice_count int          not null,
    total_score          int          not null,
    updated_at           datetime(6)  null,
    constraint username
        unique (username)
);

create table if not exists culture_favorite
(
    id           bigint auto_increment
        primary key,
    favorited_at datetime(6) not null,
    content_id   bigint      not null,
    user_id      bigint      not null,
    constraint culture_favorite_user_id_content_id_832eec51_uniq
        unique (user_id, content_id),
    constraint culture_favorite_content_id_292ae17f_fk_culture_content_id
        foreign key (content_id) references culture_content (id),
    constraint culture_favorite_user_id_54852552_fk_user_user_id
        foreign key (user_id) references user_user (id)
);

create table if not exists django_admin_log
(
    id              int auto_increment
        primary key,
    action_time     datetime(6)       not null,
    object_id       longtext          null,
    object_repr     varchar(200)      not null,
    action_flag     smallint unsigned not null,
    change_message  longtext          not null,
    content_type_id int               null,
    user_id         bigint            not null,
    constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
        foreign key (content_type_id) references django_content_type (id),
    constraint django_admin_log_user_id_c564eba6_fk_user_user_id
        foreign key (user_id) references user_user (id)
);

create table if not exists question_answerrecord
(
    id          bigint auto_increment
        primary key,
    user_answer longtext    not null,
    is_correct  tinyint(1)  not null,
    question_id bigint      not null,
    user_id     bigint      not null,
    created_at  datetime(6) not null,
    constraint question_answerrecor_question_id_38aaf7ee_fk_question_
        foreign key (question_id) references question_question (id),
    constraint question_answerrecord_user_id_175d8c4b_fk_user_user_id
        foreign key (user_id) references user_user (id)
);

create table if not exists question_wrongbook
(
    id          bigint auto_increment
        primary key,
    question_id bigint      not null,
    user_id     bigint      not null,
    created_at  datetime(6) not null,
    constraint question_wrongbook_user_id_question_id_46da17b4_uniq
        unique (user_id, question_id),
    constraint question_wrongbook_question_id_b4179ec6_fk_question_question_id
        foreign key (question_id) references question_question (id),
    constraint question_wrongbook_user_id_1c2abc82_fk_user_user_id
        foreign key (user_id) references user_user (id)
);

create table if not exists user_user_groups
(
    id       int auto_increment
        primary key,
    user_id  bigint not null,
    group_id int    not null,
    constraint user_user_groups_user_id_group_id_bb60391f_uniq
        unique (user_id, group_id),
    constraint user_user_groups_group_id_c57f13c0_fk_auth_group_id
        foreign key (group_id) references auth_group (id),
    constraint user_user_groups_user_id_13f9a20d_fk_user_user_id
        foreign key (user_id) references user_user (id)
);

create table if not exists user_user_user_permissions
(
    id            int auto_increment
        primary key,
    user_id       bigint not null,
    permission_id int    not null,
    constraint user_user_user_permissions_user_id_permission_id_64f4d5b8_uniq
        unique (user_id, permission_id),
    constraint user_user_user_permi_permission_id_ce49d4de_fk_auth_perm
        foreign key (permission_id) references auth_permission (id),
    constraint user_user_user_permissions_user_id_31782f58_fk_user_user_id
        foreign key (user_id) references user_user (id)
);


