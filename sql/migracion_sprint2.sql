-- Migración del Sprint 2 (HU-09) para una base creada con el schema del Sprint 1.
-- Si la base se crea desde cero con schema.sql, este script NO hace falta.
USE agua_cocacola;

-- 1. Borrar los duplicados que ya existan (deja el registro con el id más bajo).
DELETE c1 FROM consumos c1
JOIN consumos c2
  ON c1.proceso_id = c2.proceso_id
 AND c1.fecha = c2.fecha
 AND c1.id > c2.id;

DELETE r1 FROM referencias r1
JOIN referencias r2
  ON r1.proceso_id = r2.proceso_id
 AND r1.mes = r2.mes
 AND r1.id > r2.id;

-- 2. Agregar las restricciones únicas.
ALTER TABLE consumos
  ADD UNIQUE KEY uq_consumo_proceso_fecha (proceso_id, fecha);

ALTER TABLE referencias
  ADD UNIQUE KEY uq_referencia_proceso_mes (proceso_id, mes);
