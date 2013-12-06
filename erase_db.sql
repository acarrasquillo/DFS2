-- 
-- Usage, on terminal run:
-- mysql -u ram -p < erase_db.sql

use ccom4017_dfs_ram ;

TRUNCATE TABLE block;
TRUNCATE TABLE data_node;
TRUNCATE TABLE inode;