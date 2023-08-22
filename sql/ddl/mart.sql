create table if not exists mart.watching_movies/*ON CLUSTER cluster*/(
     id UInt32,
     user_id UUID,
     movie_id UUID,
     frameno UInt32,
     timestamp DATETIME
)
engine = MergeTree
order by id
partition by toMonth(timestamp);

create table if not exists mart.likes_movies/*ON CLUSTER cluster*/(
      movie_id UUID,
      user_id UUID,
      score UInt32,
      timestamp DATETIME
)
engine = MergeTree
order by timestamp
partition by toMonth(timestamp);
