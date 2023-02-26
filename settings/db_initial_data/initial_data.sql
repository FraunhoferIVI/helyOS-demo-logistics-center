--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12 (Debian 10.12-2.pgdg90+1)
-- Dumped by pg_dump version 10.13 (Ubuntu 10.13-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


--
-- Data for Name: work_processes; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.work_process_type 
            (name ,          description,       num_max_agents, dispatch_order, extra_params)
     VALUES   
            ('driving',        'drive from a to b',    1,           '[["A"]]' ,  NULL ),
            ('test_mission',  'drive from a to b',    1,           '[["A"]]' ,  NULL );
			

            

INSERT INTO public.work_process_service_plan 
            (work_process_type_id, step ,request_order, agent, service_type,  depends_on_steps, is_result_assignment)
     VALUES   
            (1,                    'A' ,     1,             1,    'drive',     	    '[]',          true),
            (2,                    'A' ,     1,             1,    'dummy_service', '[]',          true);


			

--
-- Data for Name: yards; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.yards DISABLE TRIGGER ALL;


INSERT INTO public.yards 
            (id, uid , name,   description,   source    ,   yard_type     ,   map_data,                                                            lat,      lon,  alt,    created_at,                      modified_at )
     VALUES   
            (1, '1','DASHSER',  'Test yard for demo', 'initial_data', 'logistic_yard', '{"origin": {"lat": 48.49099, "lon": 10.084967, "alt": 57, "zoomLevel": 19}}', 48.49099, 10.084967, 57,  '2020-08-03 12:00:00.000000', '2020-08-03 12:00:00.000000');

ALTER TABLE public.yards ENABLE TRIGGER ALL;
SELECT pg_catalog.setval('public.yards_id_seq', 2, true);

--
-- Data for Name: shapes; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.shapes DISABLE TRIGGER ALL;

--


ALTER TABLE public.shapes ENABLE TRIGGER ALL;
SELECT pg_catalog.setval('public.shapes_id_seq', 1, true);




