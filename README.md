# ResortInspector

## Iniciar conexion
c = Connection()

## Obtener perfil de hermandad
c.getGuildProfile(name="Resort", realm="C'thun", fields=["members"])

## Obtener perfil de un jugador
c.getMemberProfile(name="Raksus", realm="C'thun", fields=["items"])
