
with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),

renamed as (
    select
         CAST(dispatching_base_num AS STRING) AS dispatch_base_id
        , CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime
        , CAST(dropOff_datetime AS TIMESTAMP) AS dropoff_datetime
        , CAST(PUlocationID AS STRING) AS pickup_location_id
        , CAST(DOlocationID AS STRING) AS dropoff_location_id
        , CAST(SR_Flag AS INTEGER) AS shared_ride_flag
        , CAST(Affiliated_base_number AS STRING) AS affiliated_base_id

    from source
    -- Filter out records with null vendor_id (data quality requirement)
    where dispatching_base_num is not null
)

select * from renamed


