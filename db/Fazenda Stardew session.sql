TRUNCATE TABLE produtos RESTART IDENTITY CASCADE;
TRUNCATE TABLE categorias RESTART IDENTITY CASCADE;
TRUNCATE TABLE qualidades RESTART IDENTITY CASCADE;


INSERT INTO categorias (nome, valor_base) VALUES 
('Semente', 20.0), 
('Cultivo', 80.0), 
('Coleta', 50.0), 
('Peixe', 100.0), 
('Produto Artesanal', 300.0);


INSERT INTO qualidades (nome, multiplicador) VALUES 
('Normal', 1.0), 
('Prata', 1.25), 
('Ouro', 1.5), 
('Irídio', 2.0);


INSERT INTO produtos (nome, quantidade_estoque, id_categoria, id_qualidade) VALUES 

('Semente de Chirívia', 50, 1, 1), ('Semente de Melancia', 20, 1, 1),
('Semente de Abóbora', 15, 1, 1), ('Semente de Carambola', 10, 1, 1),
('Semente de Mirtilo', 30, 1, 1), ('Semente de Fruta Antiga', 5, 1, 1),
('Semente de Couve-Flor', 12, 1, 1), ('Semente de Oxicoco', 25, 1, 1),


('Melancia Especial', 10, 2, 4), ('Abóbora Gigante', 8, 2, 3),
('Carambola Doce', 15, 2, 4), ('Fruta Antiga Colhida', 5, 2, 3),
('Morango Silvestre', 20, 2, 2), ('Couve-Flor de Verão', 6, 2, 3),
('Batata Comum', 40, 2, 1), ('Lúpulo de Cerveja', 30, 2, 2),


('Cogumelo Roxo', 5, 3, 4), ('Trufa de Porco', 3, 3, 4),
('Amora da Floresta', 50, 3, 2), ('Framboesa de Outono', 45, 3, 1),
('Alcaparra de Inverno', 12, 3, 3), ('Raiz de Inverno', 10, 3, 2),
('Inhame de Neve', 8, 3, 1), ('Avelã da Vila', 20, 3, 3),


('Lenda do Lago', 1, 4, 4), ('Enguia de Lava', 2, 4, 4),
('Esturjão Raro', 5, 4, 3), ('Truta Arco-Íris', 10, 4, 2),
('Lula Gigante', 4, 4, 1), ('Peixe-Gato Robusto', 3, 4, 3),
('Baiacu Inflado', 6, 4, 4), ('Salmão do Rio', 15, 4, 2),


('Vinho de Fruta Antiga', 10, 5, 4), ('Vinho de Carambola', 15, 5, 3),
('Vinho de Melancia', 20, 5, 2), ('Vinho de Chirívia', 25, 5, 4),
('Vinho de Mirtilo', 12, 5, 3), ('Vinho de Couve-Flor', 8, 5, 2),
('TESTE', 18, 5, 4), ('Vinho de Fruta Antiga Colhida', 5, 5, 3);