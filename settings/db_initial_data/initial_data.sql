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
-- Data for Name: yards; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.yards DISABLE TRIGGER ALL;


INSERT INTO public.yards 
            (id, uid , name,   description,   source    ,   yard_type     ,   map_data,                                                            lat,      lon,  alt,    created_at,                      modified_at )
     VALUES   
            (1, '1', 'EMONS', 'test yard', 'initial data', 'logistic_yard', '{"origin": {"lat": 51.0531973, "lon": 13.7031056, "alt": 116, "zoomLevel": 19}}', 51.053197, 13.703106, 116, '2020-08-03 12:00:00.000000', '2020-08-03 12:00:00.000000');


ALTER TABLE public.yards ENABLE TRIGGER ALL;
SELECT pg_catalog.setval('public.yards_id_seq', 2, true);

--
-- Data for Name: shapes; Type: TABLE DATA; Schema: public; Owner: postgres
--

ALTER TABLE public.map_objects DISABLE TRIGGER ALL;

INSERT INTO public.map_objects VALUES (1, 1, '{"top": 1000000, "bottom": 0, "geometry_type" : "polygon",  "points": [
		[-26216.225821195887, 78610.13436118636],
		[-27382.334885132288, 72923.70671081838],
		[-30130.402341942776, 62154.20186352197],
		[-54108.90228931279, -28043.36591010827],
		[83896.58660178045, -67414.15481101617],
		[97311.87292192974, -19169.253660776976],
		[106931.12035607074, 20055.239628507068],
		[111767.10060930236, 35428.236363096235],
		[114225.77587464689, 41948.48874749138]
]}', 'drivable', 'trucktrix-map', '{}',  '2022-07-21 12:34:56.789000', '2022-07-21 12:34:56.789000', NULL);



INSERT INTO public.map_objects VALUES (3, 1, '{"top": 1000000, "bottom": 0, "geometry_type" : "polygon",  
              "points": [
                    [-24195.83602726925,
                        37724.81920197606],
                    [-19149.543827574234,
                        57328.39013263583],
                    [6302.453942247666,
                        50411.08353994787],
                    [2420.1872100820765,
                        32848.03724940866]
                ]}', 'obstacle', 'trucktrix-map', '{}',  '2022-07-21 12:34:56.789000', '2022-07-21 12:34:56.789000', NULL);

INSERT INTO public.map_objects VALUES (4, 1, '{"top": 1000000, "bottom": 0, "geometry_type" :  "polygon",  
                "points": [
                    [-22277.788128354587,
                        -29656.999085098505],
                    [11955.177565047052,
                        -39645.590821281075],
                    [32264.155154756736,
                        24571.038713678718],
                    [-2397.2147758468054,
                        31563.508927822113]
                ]}', 'obstacle', 'trucktrix-map', '{}',  '2022-07-21 12:34:56.789000', '2022-07-21 12:34:56.789000', NULL);

INSERT INTO public.map_objects VALUES (5, 1, '{"top": 1000000, "bottom": 0, "geometry_type" : "polygon", 
                "points": [
                    [52301.47678265348,
                        -39108.26916154474],
                    [48467.01023919741,
                        -48360.05252134055],
                    [12347.63237775769,
                        -38713.91633246094],
                    [21872.210574743804,
                        -10348.736547864974],
                    [57463.823264755774,
                        -17920.601472258568]
                ]}', 'obstacle', 'trucktrix-map', '{}',  '2022-07-21 12:34:56.789000', '2022-07-21 12:34:56.789000', NULL);
--


ALTER TABLE public.map_objects ENABLE TRIGGER ALL;
SELECT pg_catalog.setval('public.map_objects_id_seq', 8, true);




