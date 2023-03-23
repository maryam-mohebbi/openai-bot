create table if not exists MESSAGES
(
    ID                int auto_increment
        primary key,
    CHAT_ID           varchar(100)                       not null,
    USERNAME          varchar(255)                       not null,
    DATETIME          varchar(255)                       not null,
    MESSAGE_ID        varchar(100)                       not null,
    TEXT              text charset utf8mb3               not null,
    REPLY_MESSAGE_ID  varchar(100)                       null,
    COMPLETION_TOKENS int                                null,
    PROMPT_TOKENS     int                                null,
    CREATE_AT         datetime default CURRENT_TIMESTAMP not null,
    UPDATE_AT         datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create table if not exists USERS
(
    ID         int auto_increment
        primary key,
    USERNAME   varchar(100)                       not null,
    CREATED_AT datetime default CURRENT_TIMESTAMP not null,
    UPDATED_AT datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    constraint USERS_pk
        unique (USERNAME)
);

