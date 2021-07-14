-- This comment is reserved for possible syntax reference purpose.
/*
  Notifies changes in Beetle table.
 */
-- create or replace function notify_beetle_changes() returns trigger as
-- $$
-- declare
--     selected_rid varchar(20);
--     restaurant_lon float;
--     restaurant_lat float;
-- begin
--     if (new.rider_id is not null) then return null;
--     end if; -- for insertion of past orders in data.sql
--
--     select lon into restaurant_lon from Restaurants where id = new.rid;
--     select lat into restaurant_lat from Restaurants where id = new.rid;
--
--     with AvailableRiders as
--              (select rid as rider_id from PWS
--               where start_of_week + day_of_week + (start_hour || ' hour')::interval <= CURRENT_TIMESTAMP
--                 and start_of_week + day_of_week + (end_hour || ' hour')::interval > CURRENT_TIMESTAMP
--               union -- union both available part time and full time riders.
--               select rid as rider_id
--               from FWS F, Shifts S
--               where CURRENT_DATE - F.start_date < 28 and CURRENT_DATE >= F.start_date
--                 and S.shift_num = case (CURRENT_DATE - F.start_date) % 7
--                                       when 0 then F.day_one when 1 then F.day_two when 2 then F.day_three when 3 then F.day_four
--                                       when 4 then F.day_five when 5 then F.day_six when 6 then F.day_seven
--                   end
--                 and ((CURRENT_DATE + (S.first_start_hour || ' hour')::interval <= CURRENT_TIMESTAMP
--                   and CURRENT_DATE + (S.first_end_hour || ' hour')::interval > CURRENT_TIMESTAMP)
--                   or
--                      (CURRENT_DATE + (S.second_start_hour || ' hour')::interval <= CURRENT_TIMESTAMP
--                          and CURRENT_DATE + (S.second_end_hour || ' hour')::interval > CURRENT_TIMESTAMP)))
--     select A.rider_id into selected_rid
--     from AvailableRiders A join Riders R on A.rider_id = R.id
--                            left join Orders O on A.rider_id = O.rider_id -- left join to preserve riders without any deliveries
--         and O.time_delivered is null -- remove finished orders
--     group by A.rider_id, R.id
--     order by count(O.id), -- riders with less deliveries
--              point(R.lon, R.lat) <@> point(restaurant_lon, restaurant_lat) -- riders closer to the restaurant
--     limit 1; -- choose the most suitable rider.
--
--     if (selected_rid is null) then raise exception 'No rider available!';
--     end if;
--
--
--     update Orders -- write the rider id to the new order
--     set    rider_id = selected_rid
--     where  id = new.id;
--
--     return null;
-- end;
-- $$ language plpgsql;

create or replace function notify_beetle_changes() returns trigger as
$$
declare
begin
    perform pg_notify(
            'streaming_data',
            json_build_object(
                'table_name', 'Beetle',
                'record', row_to_json(new)
            )::text
        );
    return null;
end;
$$ language plpgsql;

drop trigger if exists beetle_inserted on Beetle cascade;
create trigger beetle_inserted
    after insert on Beetle
    for each row
execute function notify_beetle_changes();

create or replace function notify_emg_changes() returns trigger as
$$
declare
begin
    perform pg_notify(
            'streaming_data',
            json_build_object(
                    'table_name', 'EMG',
                    'record', row_to_json(new)
                )::text
        );
    return null;
end;
$$ language plpgsql;

drop trigger if exists emg_inserted on EMG cascade;
create trigger emg_inserted
    after insert on EMG
    for each row
execute function notify_emg_changes();

create or replace function notify_dance_move_changes() returns trigger as
$$
declare
begin
    perform pg_notify(
            'streaming_data',
            json_build_object(
                    'table_name', 'DanceMove',
                    'record', row_to_json(new)
                )::text
        );
    return null;
end;
$$ language plpgsql;

drop trigger if exists dance_move_inserted on DanceMove cascade;
create trigger dance_move_inserted
    after insert on DanceMove
    for each row
execute function notify_dance_move_changes();

create or replace function notify_dance_position_changes() returns trigger as
$$
declare
begin
    perform pg_notify(
            'streaming_data',
            json_build_object(
                    'table_name', 'DancePosition',
                    'record', row_to_json(new)
                )::text
        );
    return null;
end;
$$ language plpgsql;

drop trigger if exists dance_position_inserted on DancePosition cascade;
create trigger dance_position_inserted
    after insert on DancePosition
    for each row
execute function notify_dance_position_changes();