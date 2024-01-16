/NetgsmProject/backend 



Virtual Environment activate

windows venv\Scripts\activate
linux/mac source venv/bin/activate

pip install -r requirements.txt

python manage.py runserver

şimdilik çalıştırılması için sqlite da bıraktım mysql ayarlarım yorum satırında settings alanında

python manage.py makemigrations
python manage.py migrate


python manage.py createsuperuser 

burdan kullanıcı oluşturulup email ve password ile sisteme giriş yapılabilir