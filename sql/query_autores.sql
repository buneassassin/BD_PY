select * from titles; 
select * from sales; 

SELECT t.title_id,t.title,sum(t.price*qty) as total 
from titles as t
INNER JOIN sales as s 
on t.title_id=s.title_id 
-- where s.stor_id is NULL 
group by t.title_id
; 

SELECT sum(t.price*qty) as total 
from titles as t
INNER JOIN sales as s 
on t.title_id=s.title_id 
-- where s.stor_id is NULL 
;

select 
a.au_fname,a.au_lname, 
sum(t.price*s.qty*ta.royaltyper/100) as Total 
from titleauthor as ta 
INNER JOIN `authors` as a on a.au_id=ta.au_id
INNER join titles as t on t.title_id=ta.title_id
inner join sales as s on t.title_id=s.title_id
GROUP BY a.au_fname,a.au_lname 
; 

select sum(t.price*s.qty*ta.royaltyper/100) as Total 
from titleauthor as ta 
INNER JOIN `authors` as a on a.au_id=ta.au_id
INNER join titles as t on t.title_id=ta.title_id
inner join sales as s on t.title_id=s.title_id
; 



select t.title_id, 
ifnull(100-sum(royaltyper),100) as royalrestante,
ifnull(sum(royaltyper),0) as royal
from titles as t  
left join titleauthor as ta on ta.title_id=t.title_id
GROUP BY title_id
 HAVING royal<100
order by title_id
;
 
select sum(s.qty*t.price*fal.royalrestante/100) as totalfaltante
from sales as s 
INNER JOIN titles as t on t.title_id=s.title_id 
INNER JOIN (
select t.title_id, 
ifnull(100-sum(royaltyper),100) as royalrestante,
ifnull(sum(royaltyper),0) as royal
from titles as t  
left join titleauthor as ta on ta.title_id=t.title_id
GROUP BY title_id
 HAVING royal<100
) fal on fal.title_id=s.title_id
/*
 770.55
 2893.500000
 199.75
 
 3863.80
 */ 
 ;
 
 select sum(t.price*s.qty) 
 from titles as t 
 INNER JOIN sales as s on s.title_id=t.title_id
 left JOIN titleauthor as ta on ta.title_id=s.title_id
 where ta.au_id is null