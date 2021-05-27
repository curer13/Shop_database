declare @Authors Table(ID int,AuthorName varchar(20))
Insert @Authors(ID,AuthorName)
Values
(1,'Rajendra'),(1,'Raj')
,(2,'Sonu'),(2,'Raju')
,(3,'Akshita'),(3,'Akshu')
,(4,'Kashish'),(4,'Kusum')
select * from @Authors

SELECT DISTINCT 
       ID, 
(
    SELECT( 
        SELECT ',' + AuthorName
        FROM @Authors
        WHERE ID = t.ID FOR XML PATH('')
        )
) AS AuthorName
FROM @Authors t;
