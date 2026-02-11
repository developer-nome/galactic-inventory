
CREATE TABLE public.galactic_items (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);

CREATE TABLE public.galactic_planets (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);

CREATE TABLE public.galactic_planets_inventory (
    id integer NOT NULL,
    galactic_planet_id integer
);

CREATE TABLE public.galactic_solar_systems (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);

CREATE TABLE public.galactic_stations (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);


CREATE TABLE public.galactic_stations_inventory (
    id integer NOT NULL,
    galactic_station_id integer,
    galactic_item_id integer
);

