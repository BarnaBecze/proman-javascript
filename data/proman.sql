ALTER TABLE IF EXISTS ONLY public.board DROP CONSTRAINT IF EXISTS pk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.card DROP CONSTRAINT IF EXISTS pk_card_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.card DROP CONSTRAINT IF EXISTS fk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.card DROP CONSTRAINT IF EXISTS fk_status_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.status DROP CONSTRAINT IF EXISTS pk_status_id CASCADE;


DROP TABLE IF EXISTS public.board;
DROP SEQUENCE IF EXISTS public.board_id_seq;
CREATE TABLE board (
    id serial NOT NULL,
    title varchar UNIQUE
);

DROP TABLE IF EXISTS public.card;
DROP SEQUENCE IF EXISTS public.card_id_seq;
CREATE TABLE card (
    id serial NOT NULL,
    board_id int NOT NULL,
    title varchar UNIQUE,
    status_id int NOT NULL,
    "order" int
);

DROP TABLE IF EXISTS public.status;
DROP SEQUENCE IF EXISTS public.status_id_seq;
CREATE TABLE status (
    id serial NOT NULL,
    title varchar UNIQUE
);

ALTER TABLE ONLY board
    ADD CONSTRAINT pk_board_id PRIMARY KEY (id);
ALTER TABLE ONLY status
    ADD CONSTRAINT pk_status_id PRIMARY KEY (id);
ALTER TABLE ONLY card
    ADD CONSTRAINT pk_card_id PRIMARY KEY (id);
ALTER TABLE ONLY card
    ADD CONSTRAINT fk_board_id FOREIGN KEY (board_id) REFERENCES board(id);
ALTER TABLE ONLY card
    ADD CONSTRAINT fk_status_id FOREIGN KEY (status_id) REFERENCES status(id);
