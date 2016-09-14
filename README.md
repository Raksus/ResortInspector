# ResortInspector

## Iniciar conexion
c = Connection()

## Obtener perfil de hermandad
c.getGuildProfile(name="Resort", realm="C'thun", fields=["members"])

## Obtener perfil de un jugador
c.getMemberProfile(name="Raksus", realm="C'thun", fields=["items"])

## Postgresql
postgresql-server-dev-all 
sudo -u postgres createuser --superuser resort
sudo -u postgres psql resort
create database wow;
