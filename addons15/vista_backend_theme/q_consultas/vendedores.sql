select
    a.f210_id_cia AS cia,
    a.f210_id AS codvend,
    b.f200_razon_social AS nomvend
from t210_mm_vendedores AS a
    inner join t200_mm_terceros AS b on f200_rowid = f210_rowid_tercero
where f210_id_cia = 1