# Doggzi - Flutter fastAPI app
## Features
- user can register with email
- login(persistent using token)
- add pet
- view pets
## Requirements
Make sure you have the following installed:

- **Flutter 3.22.3**
- **Dart 3.4.4**
- **Android Studio or VS Code** (with Flutter and Dart plugins)
- **Android SDK 34**
- **Gradle 8.7**

---
## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/princesoni18/whatbytes.git
cd your-flutter-project
flutter pub get
flutter run

# for backend
```bash
cd backend
python -m venv venv
venv/scripts/activate
pip install -r reqiurements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

