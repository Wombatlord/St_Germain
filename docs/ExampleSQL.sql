INSERT INTO recipe
    (author, title, ingredients, cooktime, method, serves)
     VALUES
     ('Bezos', 'Beanz', '{"People": "All"}', '30 mins', 'friction', 'Subpoenas');

SELECT * FROM recipe;
SELECT sequence, method FROM recipe;
UPDATE recipe SET cooktime = '20 minutes' WHERE sequence = 1;

