# AI Collab Code Editor 🚀

A production-grade code collaboration platform built with FastAPI that integrates real-time collaboration, AI-powered code assistance, and robust data storage using PostgreSQL. This application leverages Redis and websockets for instant updates and OpenAI’s GPT-4 mini for contextual code suggestions—all wrapped in a clean HTML UI styled with Bootstrap.

---

## Project Structure 🌳

<!-- TREE_START -->
```
.
├── app
│   ├── code_editor
│   │   ├── code_editor_router.py
│   │   ├── code_editor_schema.py
│   │   └── code_editor_service.py
│   ├── code_session
│   │   ├── code_session_crud.py
│   │   ├── code_session_model.py
│   │   ├── code_session_router.py
│   │   ├── code_session_schema.py
│   │   └── code_session_service.py
│   ├── health
│   │   └── health_router.py
│   ├── ui
│   │   └── ui_router.py
│   ├── user
│   │   ├── user_auth.py
│   │   ├── user_crud.py
│   │   ├── user_model.py
│   │   ├── user_router.py
│   │   ├── user_schema.py
│   │   └── user_service.py
│   ├── utils
│   │   └── helper.py
│   ├── auth_dependency.py
│   ├── database.py
│   └── settings.py
├── docs
│   ├── Demo.mov
│   └── openapi.json
├── templates
│   ├── code-editor.html
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
├── CONTRIBUTORS.txt
├── Dockerfile
├── LICENSE
├── README.md
├── gunicorn_conf.py
├── main.py
├── requirements.txt
├── run.sh
└── set_env.sh
```
<!-- TREE_END -->

---

## Features ✨

- **JWT-Based Authentication** 🔐  
  Secure user sessions using token-based authentication.
  
- **Real-Time Collaboration** ⚡  
  Websockets and Redis enable instantaneous updates and collaboration.
  
- **AI-Powered Code Assistance** 🤖  
  Integrated with OpenAI’s GPT-4 mini for contextual code suggestions and improvements.
  
- **Robust Data Storage** 💾  
  PostgreSQL is used as the primary database for reliability and scalability.
  
- **Production-Ready FastAPI Backend**  
  Built with a modular architecture for scalable development.
  
- **Direct HTML UI**  
  Clean, responsive design using HTML, CSS, JavaScript, and Bootstrap.

---

## Technologies

- **Backend:** FastAPI, Uvicorn, Gunicorn
- **Database:** PostgreSQL
- **Real-Time:** Redis, Websockets
- **AI Integration:** OpenAI API (GPT-4 mini)
- **UI:** HTML, CSS, JavaScript, Bootstrap
- **Containerization:** Docker

---

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- Docker (optional)

### Environment Setup

For local development, set all environment variables in `set_env.sh` and run:

```bash
source set_env.sh
```

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/ai-collab-code-editor.git
   cd ai-collab-code-editor
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

- **Local / Development:**

  Make sure to load your environment variables:

  ```bash
  source set_env.sh
  python main.py
  ```

- **Production:**

  Use the provided `run.sh` script (which runs Gunicorn + Uvicorn):

  ```bash
  ./run.sh
  ```

---

## API Documentation

Check the full OpenAPI specification in the file:  
**`docs/openapi.json`**

Interactive API documentation is also available once the server is running:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Demo 🎥

Watch the demo video below to see AI Collab Code Editor in action:
[Download Demo Video](docs/Demo.mp4)

---

## Contributing

Contributions, bug reports, and feature suggestions are welcome. Please see [CONTRIBUTORS.txt](CONTRIBUTORS.txt) for contribution guidelines.

---

## License

This project is licensed under the [MIT License](LICENSE).

---
