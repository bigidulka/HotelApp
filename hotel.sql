--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    id integer NOT NULL,
    roomid integer NOT NULL,
    guestid integer NOT NULL,
    checkindate date NOT NULL,
    checkoutdate date
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- Name: bookings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bookings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bookings_id_seq OWNER TO postgres;

--
-- Name: bookings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bookings_id_seq OWNED BY public.bookings.id;


--
-- Name: bookingservices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookingservices (
    id integer NOT NULL,
    bookingid integer NOT NULL,
    serviceid integer NOT NULL,
    servicedate date,
    quantity integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.bookingservices OWNER TO postgres;

--
-- Name: bookingservices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bookingservices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bookingservices_id_seq OWNER TO postgres;

--
-- Name: bookingservices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bookingservices_id_seq OWNED BY public.bookingservices.id;


--
-- Name: cleaningschedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cleaningschedule (
    id integer NOT NULL,
    roomid integer NOT NULL,
    staffid integer NOT NULL,
    cleaningdate date NOT NULL
);


ALTER TABLE public.cleaningschedule OWNER TO postgres;

--
-- Name: cleaningschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cleaningschedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cleaningschedule_id_seq OWNER TO postgres;

--
-- Name: cleaningschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cleaningschedule_id_seq OWNED BY public.cleaningschedule.id;


--
-- Name: guests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.guests (
    id integer NOT NULL,
    fullname character varying(100) NOT NULL,
    passportdata character varying(50)
);


ALTER TABLE public.guests OWNER TO postgres;

--
-- Name: guests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.guests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.guests_id_seq OWNER TO postgres;

--
-- Name: guests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.guests_id_seq OWNED BY public.guests.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    "RoleId" integer NOT NULL,
    rolename character varying(50) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles."RoleId";


--
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    id integer NOT NULL,
    floor integer NOT NULL,
    category character varying(100) NOT NULL,
    statusid integer DEFAULT 1 NOT NULL,
    roomnumber integer
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- Name: rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rooms_id_seq OWNER TO postgres;

--
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_id_seq OWNED BY public.rooms.id;


--
-- Name: roomstatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roomstatus (
    id integer NOT NULL,
    statusname character varying(50) NOT NULL
);


ALTER TABLE public.roomstatus OWNER TO postgres;

--
-- Name: roomstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roomstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roomstatus_id_seq OWNER TO postgres;

--
-- Name: roomstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roomstatus_id_seq OWNED BY public.roomstatus.id;


--
-- Name: services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.services (
    id integer NOT NULL,
    servicename character varying(100) NOT NULL,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.services OWNER TO postgres;

--
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.services_id_seq OWNER TO postgres;

--
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- Name: staff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff (
    id integer NOT NULL,
    fullname character varying(100) NOT NULL,
    roleid integer NOT NULL
);


ALTER TABLE public.staff OWNER TO postgres;

--
-- Name: staff_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.staff_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.staff_id_seq OWNER TO postgres;

--
-- Name: staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.staff_id_seq OWNED BY public.staff.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    login character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    isblocked boolean DEFAULT false NOT NULL,
    lastlogin timestamp without time zone,
    passwordchanged boolean DEFAULT false NOT NULL,
    failedloginattempts integer DEFAULT 0 NOT NULL,
    createdat timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "RoleID" integer NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_userid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_userid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_userid_seq OWNER TO postgres;

--
-- Name: users_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_userid_seq OWNED BY public.users.userid;


--
-- Name: bookings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings ALTER COLUMN id SET DEFAULT nextval('public.bookings_id_seq'::regclass);


--
-- Name: bookingservices id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookingservices ALTER COLUMN id SET DEFAULT nextval('public.bookingservices_id_seq'::regclass);


--
-- Name: cleaningschedule id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cleaningschedule ALTER COLUMN id SET DEFAULT nextval('public.cleaningschedule_id_seq'::regclass);


--
-- Name: guests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guests ALTER COLUMN id SET DEFAULT nextval('public.guests_id_seq'::regclass);


--
-- Name: roles RoleId; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN "RoleId" SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: rooms id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN id SET DEFAULT nextval('public.rooms_id_seq'::regclass);


--
-- Name: roomstatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomstatus ALTER COLUMN id SET DEFAULT nextval('public.roomstatus_id_seq'::regclass);


--
-- Name: services id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- Name: staff id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff ALTER COLUMN id SET DEFAULT nextval('public.staff_id_seq'::regclass);


--
-- Name: users userid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN userid SET DEFAULT nextval('public.users_userid_seq'::regclass);


--
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookings (id, roomid, guestid, checkindate, checkoutdate) FROM stdin;
1	1	1	2025-02-14	2025-03-02
2	2	2	2025-02-28	\N
3	4	3	2025-02-23	2025-02-02
4	5	5	2025-02-24	2025-03-17
5	7	6	2025-02-28	2025-03-15
\.


--
-- Data for Name: bookingservices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookingservices (id, bookingid, serviceid, servicedate, quantity) FROM stdin;
\.


--
-- Data for Name: cleaningschedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cleaningschedule (id, roomid, staffid, cleaningdate) FROM stdin;
\.


--
-- Data for Name: guests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.guests (id, fullname, passportdata) FROM stdin;
1	Шевченко Ольга Викторовна	1234 567890
2	Мазалова Ирина Львовна	2345 678901
3	Семеняка Юрий Геннадьевич	3456 789012
4	Бахшиев Павел Иннокентьевич	4567 890123
5	Мазалова Ольга Николаевна	5678 901234
6	Филь Марина Федоровна	6789 012345
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles ("RoleId", rolename) FROM stdin;
1	Администратор
2	Пользователь
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (id, floor, category, statusid, roomnumber) FROM stdin;
1	1	Одноместный стандарт	1	\N
2	1	Одноместный стандарт	1	\N
3	1	Одноместный эконом	2	\N
4	1	Одноместный эконом	1	\N
5	2	Бизнес с 1 или 2 кроватями	1	\N
6	3	Студия	3	\N
7	3	Люкс с 2 двуспальными кроватями	1	\N
36	1	Одноместный стандарт	2	101
37	1	Одноместный стандарт	2	102
38	1	Одноместный эконом	2	103
39	1	Одноместный эконом	2	104
40	1	Стандарт двухместный с 2 раздельными кроватями	2	105
41	1	Стандарт двухместный с 2 раздельными кроватями	2	106
42	1	Эконом двухместный с 2 раздельными кроватями	2	107
43	1	Эконом двухместный с 2 раздельными кроватями	2	108
44	1	3-местный бюджет	2	109
45	1	3-местный бюджет	2	110
46	2	Бизнес с 1 или 2 кроватями	2	201
47	2	Бизнес с 1 или 2 кроватями	2	202
48	2	Бизнес с 1 или 2 кроватями	2	203
49	2	Двухкомнатный двухместный стандарт с 1 или 2 кроватями	2	204
50	2	Двухкомнатный двухместный стандарт с 1 или 2 кроватями	2	205
51	2	Двухкомнатный двухместный стандарт с 1 или 2 кроватями	2	206
52	2	Одноместный стандарт	2	207
53	2	Одноместный стандарт	2	208
54	2	Одноместный стандарт	2	209
55	3	Студия	2	301
56	3	Студия	2	302
57	3	Студия	2	303
58	3	Люкс с 2 двуспальными кроватями	2	304
59	3	Люкс с 2 двуспальными кроватями	2	305
60	3	Люкс с 2 двуспальными кроватями	2	306
\.


--
-- Data for Name: roomstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roomstatus (id, statusname) FROM stdin;
1	Занят
2	Чистый
3	Грязный
4	Назначен к уборке
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.services (id, servicename, price) FROM stdin;
\.


--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staff (id, fullname, roleid) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--
    
COPY public.users (userid, login, password, isblocked, lastlogin, passwordchanged, failedloginattempts, createdat, "RoleID") FROM stdin;
2	user1	$2b$12$wKWcNdQV9XSWx.uniqmxdOS6sWgZIXxKvLsESAJ81dbnlyN08y9Ni	f	2025-03-23 18:19:50.387934	f	0	2025-03-22 17:19:01.34041	2
1	admin	$2b$12$e6ME6rmriOSEw5kN8UP3x.FGvNTaagTMKB4qaMePn5SJ5CyRm//De	f	2025-03-26 14:24:08.931142	t	0	2025-03-22 17:19:01.34041	1
\.


--
-- Name: bookings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookings_id_seq', 5, true);


--
-- Name: bookingservices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookingservices_id_seq', 1, false);


--
-- Name: cleaningschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cleaningschedule_id_seq', 1, false);


--
-- Name: guests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.guests_id_seq', 6, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 2, true);


--
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_id_seq', 63, true);


--
-- Name: roomstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roomstatus_id_seq', 4, true);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.services_id_seq', 1, false);


--
-- Name: staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.staff_id_seq', 1, false);


--
-- Name: users_userid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_userid_seq', 2, true);


--
-- Name: bookings bookings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (id);


--
-- Name: bookingservices bookingservices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookingservices
    ADD CONSTRAINT bookingservices_pkey PRIMARY KEY (id);


--
-- Name: cleaningschedule cleaningschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cleaningschedule
    ADD CONSTRAINT cleaningschedule_pkey PRIMARY KEY (id);


--
-- Name: guests guests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guests
    ADD CONSTRAINT guests_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY ("RoleId");


--
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);


--
-- Name: roomstatus roomstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roomstatus
    ADD CONSTRAINT roomstatus_pkey PRIMARY KEY (id);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (id);


--
-- Name: users users_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- Name: bookings bookings_guestid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_guestid_fkey FOREIGN KEY (guestid) REFERENCES public.guests(id) ON DELETE RESTRICT;


--
-- Name: bookings bookings_roomid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT bookings_roomid_fkey FOREIGN KEY (roomid) REFERENCES public.rooms(id) ON DELETE RESTRICT;


--
-- Name: bookingservices bookingservices_bookingid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookingservices
    ADD CONSTRAINT bookingservices_bookingid_fkey FOREIGN KEY (bookingid) REFERENCES public.bookings(id) ON DELETE CASCADE;


--
-- Name: bookingservices bookingservices_serviceid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookingservices
    ADD CONSTRAINT bookingservices_serviceid_fkey FOREIGN KEY (serviceid) REFERENCES public.services(id) ON DELETE RESTRICT;


--
-- Name: cleaningschedule cleaningschedule_roomid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cleaningschedule
    ADD CONSTRAINT cleaningschedule_roomid_fkey FOREIGN KEY (roomid) REFERENCES public.rooms(id) ON DELETE RESTRICT;


--
-- Name: cleaningschedule cleaningschedule_staffid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cleaningschedule
    ADD CONSTRAINT cleaningschedule_staffid_fkey FOREIGN KEY (staffid) REFERENCES public.staff(id) ON DELETE RESTRICT;


--
-- Name: users fk_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_role FOREIGN KEY ("RoleID") REFERENCES public.roles("RoleId") ON DELETE RESTRICT;


--
-- Name: rooms rooms_statusid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_statusid_fkey FOREIGN KEY (statusid) REFERENCES public.roomstatus(id) ON DELETE RESTRICT;


--
-- Name: staff staff_roleid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_roleid_fkey FOREIGN KEY (roleid) REFERENCES public.roles("RoleId") ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

