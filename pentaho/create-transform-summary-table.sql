CREATE TABLE public.transformation_summary (
    id serial4 NOT NULL,
    run_name varchar(159) NULL,
    pathname varchar(100) NULL,
    filename varchar(100) NULL,
    summary_result text NULL,
    model varchar(159) NULL,
    temperature numeric NULL,
    request_content text NULL,
    run_datetime timestamp NULL,
    CONSTRAINT transformation_summary_pkey PRIMARY KEY (id)
);