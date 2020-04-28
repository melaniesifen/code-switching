/* for table in database:
    get percent of rows with lang = "both" cs_reason = "lexical need"
    ....
    put all into another table */

USE textdatabase

CREATE TABLE cs_results (
    title varchar(80),
    lexical DECIMAL(4, 2),
    emphasis DECIMAL(4, 2),
    quote DECIMAL(4, 2),
    style DECIMAL(4, 2)

);

INSERT INTO cs_results (title)
select table_name
from information_schema.tables
where table_schema = "textdatabase" and table_name != "cs_results";


