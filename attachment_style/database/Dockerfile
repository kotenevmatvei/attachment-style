FROM postgres:16

# Install build dependencies and pg_cron
RUN apt-get update && apt-get install -y \
    postgresql-16-cron \
    && rm -rf /var/lib/apt/lists/*

# Enable pg_cron in PostgreSQL config
RUN echo "shared_preload_libraries = 'pg_cron'" >> /usr/share/postgresql/postgresql.conf.sample
