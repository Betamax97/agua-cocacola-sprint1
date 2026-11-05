-- HU-04: valores de referencia mensual por proceso (datos simulados, en m3).
-- Elegidos para que septiembre de 2026 tenga los tres escenarios de prueba:
--   tratamiento_residuales -> desviación leve      (+1,53 %)
--   refrigeracion          -> desviación moderada  (+7,13 %)
--   lavado_envases         -> desviación crítica   (+17,92 %)
--   limpieza_maquinaria y mantenimiento -> por debajo de la referencia
-- Pendiente: validar estos valores con la docente.
USE agua_cocacola;

INSERT INTO referencias (proceso_id, mes, valor_m3)
SELECT id, '2026-09', v.valor
FROM procesos p
JOIN (
  SELECT 'lavado_envases' AS nombre, 432.00 AS valor UNION ALL
  SELECT 'limpieza_maquinaria', 185.00 UNION ALL
  SELECT 'refrigeracion', 320.00 UNION ALL
  SELECT 'mantenimiento', 120.00 UNION ALL
  SELECT 'tratamiento_residuales', 380.00
) v ON v.nombre = p.nombre
ON DUPLICATE KEY UPDATE valor_m3 = VALUES(valor_m3);
