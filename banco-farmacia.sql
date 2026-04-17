CREATE TABLE farmacia ( 
 tel_farmacia INT,  
 nome_farmacia INT,  
 end_farmacia INT,  
 CNPJ_farmacia INT PRIMARY KEY  
); 

CREATE TABLE produto ( 
 qtd_produto INT,  
 valor_produto INT,  
 cod_produto INT PRIMARY KEY,  
 idfarmacia INT
); 

CREATE TABLE farmaceutico ( 
 nome_farmaceutico INT,  
 RG_farmaceutico INT PRIMARY KEY,  
 idfarmacia INT
); 

ALTER TABLE produto ADD FOREIGN KEY(idfarmacia) REFERENCES farmacia (idfarmacia);
ALTER TABLE farmaceutico ADD FOREIGN KEY(idfarmacia) REFERENCES farmacia (idfarmacia);
