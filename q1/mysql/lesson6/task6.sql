-- Задание 2
-- Пусть задан некоторый пользователь. 
-- Из всех друзей этого пользователя найдите человека, который больше всех общался с нашим пользователем.

-- 1. Через COUNT и LIMIT
SELECT from_user_id, COUNT(id) AS message_cnt
  FROM message
 WHERE (from_user_id IN
 	   (
 	   	SELECT IF(from_user_id = 99, to_user_id, from_user_id) AS user_friend
  		  FROM friend_request
 		 WHERE (from_user_id = 99 OR to_user_id = 99) 
 		   AND status = 1
 	   ) 
   AND to_user_id = 99)
 GROUP BY from_user_id
 ORDER BY message_cnt DESC
 LIMIT 1;

-- from_user_id|message_cnt|
-- ------------|-----------|
--           71|          3|

-- 2. С помощью запроса ниже объединил исходщие/входящие сообщения пользователя 99 с друзьями, то есть находим пользователя, с которым велась
--    самая активная переписка. Во обоих результатах это пользователь 71
WITH user_friend AS 
(
	SELECT IF(from_user_id = 99, to_user_id, from_user_id) AS user_friend
  	  FROM friend_request
 	 WHERE (from_user_id = 99 OR to_user_id = 99) 
 	   AND status = 1
)

SELECT from_user_id, 
	   COUNT(id) AS message_cnt,
	   CONCAT(IF(from_user_id = 99, from_user_id, to_user_id), ' ', IF(from_user_id != 99, from_user_id, to_user_id)) AS message_info
  FROM message
 WHERE (from_user_id IN (SELECT * FROM user_friend) AND to_user_id = 99)
    OR (to_user_id IN (SELECT * FROM user_friend) AND from_user_id = 99)
 GROUP BY message_info
 ORDER BY message_cnt DESC
 LIMIT 1;

-- from_user_id|message_cnt|message_info|
-- ------------|-----------|------------|
--           71|          5|99 71       |

-- Задание 3
-- Подсчитать общее количество лайков, которые получили 10 самых молодых пользователей

SELECT COUNT(*) AS c_like
  FROM `like` l
 WHERE l.user_id IN 
	   (SELECT *
	     FROM 
	     (SELECT user_id
  			FROM profile
 		   ORDER BY birthday DESC
 		   LIMIT 10
	     ) u
	   );

-- c_like|
-- ------|
--      9|

-- Задание 4
-- Определить кто больше поставил лайков (всего) - мужчины или женщины?

SELECT COUNT(user_id) AS like_count, 
	   (SELECT gender FROM profile p WHERE p.user_id = l.user_id) AS gender 
  FROM `like` l
 GROUP BY gender;
 
--  like_count|gender|
--  ----------|------|
--          56|f     |
--          44|m     |

-- Задание 5 
-- Найти 10 пользователей, которые проявляют наименьшую активность в использовании социальной сети.
-- Для решения задачи посчитаем cумму показателей пользователя:
-- - сколько загрузил медиа
-- - сколько опубликовал постов
-- - сколько сообществ, в которых он является участником
-- - сколько он написал сообщений
-- - сколько поставил лайков
-- - сколько имеет друзей

SELECT user_id,
	   (SELECT COUNT(id) FROM media m WHERE m.user_id = p.user_id) +
	   (SELECT COUNT(id) FROM post p2 WHERE p2.user_id = p.user_id) + 
	   (SELECT COUNT(community_id) FROM user_community uc WHERE uc.user_id = p.user_id) +
	   (SELECT COUNT(id) FROM message m2 WHERE m2.from_user_id = p.user_id) +
	   (SELECT COUNT(*) FROM `like` l2 WHERE l2.user_id = p.user_id) +
	   (SELECT COUNT(*) FROM friend_request fr WHERE (fr.from_user_id = p.user_id OR fr.to_user_id = p.user_id) AND fr.status = 1)
	   AS activity
  FROM profile p
 ORDER BY activity
 LIMIT 10;

 