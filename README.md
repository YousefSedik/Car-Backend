بالاصلاه علي النبي اول حاجه تعمل فايل اسمه .env

وتحط فيه حاجه زي كدا 
```
DATABASE_URL=postgresql+asyncpg://postgres:<'your postgres Password'>@localhost:5432/<'database name '>
SECRET_KEY=dadcfead7e3e6beb6a700a9ea13c624b88c4a34e4afce32e3cf7cdcc7970c97f
ALGORITHM=HS256
```
تاني حاجه هتعمل 
virtual evironment 
```
py -m venv venv 
```
تالت حاجه هتفعل ال 
virtual environment 
```
.\venv\Scripts\activate
```
رابع حاجه هتنزل ال 
dependencies
```
pip install -r requirements.txt
```
بعد كدا هتعمل 
migrate database 
و غالبا هيضرب ايرور فا شيل 
+asyncpg
من ال DATABASE_URL
و جرب تاني المفروض تشتغل بعد كدا ابقي رجع 
+asyncpg
تاني
و ابقي اعمل 
new terminal
كل مره

```
alembic upgrade head
```
بعد كدا تشغل السيرفر
```
uvicorn main:app --reload 
```
بس كدا الموضوع بسيط والله