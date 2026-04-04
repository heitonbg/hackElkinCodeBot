# ============================================================================
# ПРОФЕССИИ — 300+ ролей в 30 категориях
# ============================================================================
PROFESSIONS = {
    "it_and_development": {"name": "IT и разработка", "roles": [
        {"id": "python_dev", "title": "Python-разработчик", "skills": ["Python", "SQL", "Git", "Docker", "REST API", "PostgreSQL"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "frontend_dev", "title": "Frontend-разработчик", "skills": ["JavaScript", "HTML/CSS", "React", "TypeScript", "Git", "Webpack"], "salary_junior": "50 000 - 80 000 ₽", "salary_middle": "100 000 - 180 000 ₽"},
        {"id": "backend_dev", "title": "Backend-разработчик", "skills": ["Java", "Spring", "SQL", "Git", "Docker", "REST API"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 220 000 ₽"},
        {"id": "fullstack_dev", "title": "Fullstack-разработчик", "skills": ["JavaScript", "Python", "React", "SQL", "Git", "Docker"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "140 000 - 230 000 ₽"},
        {"id": "mobile_dev_android", "title": "Android-разработчик", "skills": ["Kotlin", "Java", "Android SDK", "Git", "REST API", "MVVM"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "mobile_dev_ios", "title": "iOS-разработчик", "skills": ["Swift", "SwiftUI", "Xcode", "Git", "REST API", "UIKit"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 210 000 ₽"},
        {"id": "golang_dev", "title": "Go-разработчик", "skills": ["Go", "Docker", "Kubernetes", "Git", "REST API", "PostgreSQL"], "salary_junior": "80 000 - 110 000 ₽", "salary_middle": "150 000 - 250 000 ₽"},
        {"id": "rust_dev", "title": "Rust-разработчик", "skills": ["Rust", "Git", "Linux", "Docker", "REST API", "PostgreSQL"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "160 000 - 280 000 ₽"},
        {"id": "csharp_dev", "title": "C#/.NET разработчик", "skills": ["C#", ".NET", "SQL", "Git", "REST API", "Entity Framework"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "php_dev", "title": "PHP-разработчик", "skills": ["PHP", "Laravel", "MySQL", "Git", "REST API", "Docker"], "salary_junior": "50 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "nodejs_dev", "title": "Node.js-разработчик", "skills": ["JavaScript", "Node.js", "Express", "MongoDB", "Git", "REST API"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "110 000 - 190 000 ₽"},
        {"id": "java_dev", "title": "Java-разработчик", "skills": ["Java", "Spring", "SQL", "Git", "Docker", "Maven"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 220 000 ₽"},
        {"id": "cpp_dev", "title": "C++ разработчик", "skills": ["C++", "Linux", "Git", "Makefile", "STL", "OpenGL"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "140 000 - 230 000 ₽"},
        {"id": "devops_engineer", "title": "DevOps-инженер", "skills": ["Docker", "Kubernetes", "Linux", "CI/CD", "Git", "Terraform"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "160 000 - 280 000 ₽"},
        {"id": "qa_manual", "title": "Ручной тестировщик (QA)", "skills": ["Тестирование", "SQL", "Jira", "Git", "Postman", "Тест-дизайн"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "qa_automation", "title": "Автоматизатор тестирования", "skills": ["Python", "Selenium", "API тестирование", "Git", "Docker", "CI/CD"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 200 000 ₽"},
        {"id": "data_engineer", "title": "Data Engineer", "skills": ["Python", "SQL", "Spark", "Kafka", "Airflow", "Docker"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "160 000 - 280 000 ₽"},
        {"id": "ml_engineer", "title": "ML-инженер", "skills": ["Python", "TensorFlow", "PyTorch", "SQL", "Docker", "Git"], "salary_junior": "90 000 - 130 000 ₽", "salary_middle": "180 000 - 300 000 ₽"},
        {"id": "game_dev", "title": "Game Developer", "skills": ["C#", "Unity", "C++", "Unreal Engine", "Git", "3D математика"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "blockchain_dev", "title": "Blockchain-разработчик", "skills": ["Solidity", "Web3", "JavaScript", "Git", "Ethereum", "Smart Contracts"], "salary_junior": "100 000 - 150 000 ₽", "salary_middle": "200 000 - 350 000 ₽"},
        {"id": "embedded_dev", "title": "Embedded-разработчик", "skills": ["C", "C++", "ARM", "Linux", "Git", "RTOS"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 220 000 ₽"},
        {"id": "security_engineer", "title": "Инженер по кибербезопасности", "skills": ["Linux", "Networking", "Python", "Nmap", "Wireshark", "Penetration Testing"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "160 000 - 280 000 ₽"},
        {"id": "sre_engineer", "title": "SRE-инженер", "skills": ["Linux", "Docker", "Kubernetes", "Python", "Monitoring", "Git"], "salary_junior": "90 000 - 130 000 ₽", "salary_middle": "170 000 - 290 000 ₽"},
        {"id": "cloud_engineer", "title": "Cloud-инженер", "skills": ["AWS", "Azure", "Terraform", "Docker", "Linux", "Python"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "160 000 - 270 000 ₽"},
        {"id": "sysadmin", "title": "Системный администратор", "skills": ["Linux", "Windows Server", "Networking", "Docker", "Git", "Bash"], "salary_junior": "50 000 - 70 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
    ]},
    "design_and_creative": {"name": "Дизайн и креатив", "roles": [
        {"id": "ui_designer", "title": "UI-дизайнер", "skills": ["Figma", "Photoshop", "Прототипирование", "Типографика", "Цвет", "Композиция"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 160 000 ₽"},
        {"id": "ux_designer", "title": "UX-дизайнер", "skills": ["Figma", "User Research", "A/B тестирование", "Прототипирование", "Wireframes", "Аналитика"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "product_designer", "title": "Product-дизайнер", "skills": ["Figma", "UX/UI", "User Research", "Прототипирование", "Дизайн-системы", "Аналитика"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "graphic_designer", "title": "Графический дизайнер", "skills": ["Photoshop", "Illustrator", "InDesign", "Типографика", "Цвет", "Брендинг"], "salary_junior": "40 000 - 65 000 ₽", "salary_middle": "70 000 - 130 000 ₽"},
        {"id": "motion_designer", "title": "Motion-дизайнер", "skills": ["After Effects", "Premiere Pro", "Cinema 4D", "Анимация", "Композиция", "Цвет"], "salary_junior": "50 000 - 80 000 ₽", "salary_middle": "90 000 - 160 000 ₽"},
        {"id": "3d_designer", "title": "3D-дизайнер", "skills": ["Blender", "3ds Max", "Maya", "ZBrush", "Текстурирование", "Рендеринг"], "salary_junior": "50 000 - 80 000 ₽", "salary_middle": "100 000 - 180 000 ₽"},
        {"id": "web_designer", "title": "Веб-дизайнер", "skills": ["Figma", "HTML/CSS", "Photoshop", "Прототипирование", "Адаптивный дизайн", "UX"], "salary_junior": "45 000 - 70 000 ₽", "salary_middle": "80 000 - 140 000 ₽"},
        {"id": "brand_designer", "title": "Бренд-дизайнер", "skills": ["Illustrator", "Photoshop", "Брендинг", "Типографика", "Логотипы", "Айдентика"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "illustrator", "title": "Иллюстратор", "skills": ["Photoshop", "Illustrator", "Рисование", "Цифровая живопись", "Композиция", "Цвет"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "game_designer", "title": "Гейм-дизайнер", "skills": ["Unity", "Game Mechanics", "Балансировка", "UX", "Прототипирование", "Аналитика"], "salary_junior": "50 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "art_director", "title": "Арт-директор", "skills": ["Photoshop", "Иллюстратор", "Брендинг", "Управление командой", "Креатив", "Презентации"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "150 000 - 250 000 ₽"},
        {"id": "interior_designer", "title": "Дизайнер интерьера", "skills": ["AutoCAD", "3ds Max", "SketchUp", "Композиция", "Цвет", "Эргономика"], "salary_junior": "40 000 - 65 000 ₽", "salary_middle": "80 000 - 140 000 ₽"},
    ]},
    "data_and_analytics": {"name": "Аналитика и данные", "roles": [
        {"id": "data_analyst", "title": "Аналитик данных", "skills": ["SQL", "Python", "Excel", "Pandas", "Power BI", "Tableau"], "salary_junior": "60 000 - 85 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "business_analyst", "title": "Бизнес-аналитик", "skills": ["SQL", "Excel", "BPMN", "UML", "Agile", "Требования"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "financial_analyst", "title": "Финансовый аналитик", "skills": ["Excel", "Финансовый анализ", "SQL", "Power BI", "Бухгалтерия", "Статистика"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "data_scientist", "title": "Data Scientist", "skills": ["Python", "SQL", "Machine Learning", "Pandas", "TensorFlow", "Статистика"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "160 000 - 280 000 ₽"},
        {"id": "marketing_analyst", "title": "Маркетинговый аналитик", "skills": ["Google Analytics", "Excel", "SQL", "A/B тестирование", "Power BI", "Статистика"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "product_analyst", "title": "Продуктовый аналитик", "skills": ["SQL", "Python", "A/B тестирование", "Excel", "Amplitude", "Статистика"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 210 000 ₽"},
        {"id": "systems_analyst", "title": "Системный аналитик", "skills": ["SQL", "BPMN", "UML", "REST API", "Jira", "Документооборот"], "salary_junior": "65 000 - 90 000 ₽", "salary_middle": "120 000 - 190 000 ₽"},
        {"id": "risk_analyst", "title": "Риск-аналитик", "skills": ["SQL", "Python", "Excel", "Статистика", "Риск-модели", "Power BI"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 210 000 ₽"},
    ]},
    "marketing_and_sales": {"name": "Маркетинг и продажи", "roles": [
        {"id": "digital_marketer", "title": "Digital-маркетолог", "skills": ["SEO", "Контекстная реклама", "SMM", "Google Analytics", "Контент-маркетинг", "A/B тестирование"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 160 000 ₽"},
        {"id": "seo_specialist", "title": "SEO-специалист", "skills": ["SEO", "Яндекс.Вебмастер", "Google Search Console", "Контент", "Аналитика", "Технический SEO"], "salary_junior": "45 000 - 70 000 ₽", "salary_middle": "80 000 - 140 000 ₽"},
        {"id": "smm_manager", "title": "SMM-менеджер", "skills": ["Instagram", "VK", "Telegram", "Контент-план", "Копирайтинг", "Таргет"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "65 000 - 120 000 ₽"},
        {"id": "content_manager", "title": "Контент-менеджер", "skills": ["Копирайтинг", "SEO", "WordPress", "Контент-план", "SMM", "Редактура"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 100 000 ₽"},
        {"id": "email_marketer", "title": "Email-маркетолог", "skills": ["Email-рассылки", "A/B тестирование", "Сегментация", "Автоматизация", "Аналитика", "Копирайтинг"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "75 000 - 130 000 ₽"},
        {"id": "ppc_specialist", "title": "PPC-специалист", "skills": ["Google Ads", "Яндекс.Директ", "Аналитика", "A/B тестирование", "Конверсия", "Бюджетирование"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "sales_manager_b2b", "title": "Менеджер по продажам B2B", "skills": ["B2B продажи", "CRM", "Переговоры", "Холодные звонки", "Презентации", "Документооборот"], "salary_junior": "50 000 - 80 000 ₽", "salary_middle": "100 000 - 180 000 ₽"},
        {"id": "sales_manager_b2c", "title": "Менеджер по продажам B2C", "skills": ["Продажи", "CRM", "Коммуникация", "Работа с возражениями", "Презентации", "Клиентоориентированность"], "salary_junior": "40 000 - 65 000 ₽", "salary_middle": "70 000 - 130 000 ₽"},
        {"id": "account_manager", "title": "Аккаунт-менеджер", "skills": ["CRM", "Переговоры", "Клиентоориентированность", "Презентации", "Аналитика", "Коммуникация"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "business_dev_manager", "title": "Менеджер по развитию бизнеса", "skills": ["Стратегия", "Переговоры", "Аналитика", "Партнёрства", "Презентации", "CRM"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "pr_manager", "title": "PR-менеджер", "skills": ["PR", "Копирайтинг", "Медиа-планирование", "Кризис-коммуникации", "Пресс-релизы", "Аналитика"], "salary_junior": "45 000 - 70 000 ₽", "salary_middle": "80 000 - 140 000 ₽"},
        {"id": "brand_manager", "title": "Бренд-менеджер", "skills": ["Бренд-стратегия", "Маркетинг", "Аналитика", "Исследования", "Презентации", "Бюджетирование"], "salary_junior": "55 000 - 85 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "event_manager", "title": "Event-менеджер", "skills": ["Организация мероприятий", "Логистика", "Переговоры", "Бюджетирование", "Координация", "Коммуникация"], "salary_junior": "40 000 - 65 000 ₽", "salary_middle": "75 000 - 130 000 ₽"},
    ]},
    "management": {"name": "Управление", "roles": [
        {"id": "project_manager", "title": "Project-менеджер", "skills": ["Agile", "Scrum", "Jira", "Планирование", "Коммуникация", "Бюджетирование"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "product_manager", "title": "Product-менеджер", "skills": ["Product-стратегия", "User Research", "A/B тестирование", "Аналитика", "Roadmap", "Приоритизация"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "160 000 - 280 000 ₽"},
        {"id": "scrum_master", "title": "Scrum-мастер", "skills": ["Scrum", "Agile", "Facilitation", "Jira", "Коммуникация", "Коучинг"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 210 000 ₽"},
        {"id": "team_lead", "title": "Team Lead", "skills": ["Управление командой", "Техническая экспертиза", "Менторство", "Планирование", "Коммуникация", "Agile"], "salary_junior": "120 000 - 180 000 ₽", "salary_middle": "200 000 - 350 000 ₽"},
        {"id": "tech_lead", "title": "Tech Lead", "skills": ["Архитектура", "Code Review", "Менторство", "Техническая экспертиза", "Планирование", "Agile"], "salary_junior": "130 000 - 190 000 ₽", "salary_middle": "220 000 - 380 000 ₽"},
        {"id": "cto", "title": "CTO", "skills": ["Стратегия", "Архитектура", "Управление", "Бюджетирование", "Технологии", "Лидерство"], "salary_junior": "200 000 - 300 000 ₽", "salary_middle": "350 000 - 600 000 ₽"},
        {"id": "office_manager", "title": "Офис-менеджер", "skills": ["Администрирование", "Документооборот", "Коммуникация", "Организация", "Excel", "Координация"], "salary_junior": "35 000 - 50 000 ₽", "salary_middle": "55 000 - 80 000 ₽"},
        {"id": "executive_assistant", "title": "Личный помощник руководителя", "skills": ["Администрирование", "Документооборот", "Планирование", "Коммуникация", "Конфиденциальность", "Excel"], "salary_junior": "45 000 - 70 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
    ]},
    "hr_and_recruitment": {"name": "HR и рекрутинг", "roles": [
        {"id": "recruiter", "title": "Рекрутер", "skills": ["Подбор персонала", "Сорсинг", "Интервью", "HR-аналитика", "CRM", "Коммуникация"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "hr_manager", "title": "HR-менеджер", "skills": ["HR-политики", "Адаптация", "Обучение", "Оценка персонала", "Документооборот", "Коммуникация"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "hr_business_partner", "title": "HR Business Partner", "skills": ["HR-стратегия", "Бизнес-аналитика", "Управление изменениями", "Коммуникация", "Оценка персонала", "Развитие"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "150 000 - 250 000 ₽"},
        {"id": "talent_acquisition", "title": "Talent Acquisition", "skills": ["Сорсинг", "Подбор", "Employer Branding", "Аналитика", "Интервью", "CRM"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "learning_dev", "title": "Специалист по обучению (L&D)", "skills": ["Обучение", "Разработка программ", "E-learning", "Оценка", "Презентации", "Коммуникация"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "compensation_benefits", "title": "Специалист по компенсациям и льготам", "skills": ["HR-аналитика", "Excel", "Бюджетирование", "Бенчмаркинг", "Документооборот", "Аналитика"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "hr_analyst", "title": "HR-аналитик", "skills": ["HR-аналитика", "SQL", "Excel", "Power BI", "Статистика", "Дашборды"], "salary_junior": "60 000 - 85 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
    ]},
    "finance_and_accounting": {"name": "Финансы и бухгалтерия", "roles": [
        {"id": "accountant", "title": "Бухгалтер", "skills": ["1С", "Бухгалтерский учёт", "Налоги", "Excel", "Отчётность", "Документооборот"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "chief_accountant", "title": "Главный бухгалтер", "skills": ["Бухгалтерский учёт", "Налоги", "1С", "Отчётность", "Аудит", "Управление"], "salary_junior": "80 000 - 120 000 ₽", "salary_middle": "140 000 - 230 000 ₽"},
        {"id": "auditor", "title": "Аудитор", "skills": ["Аудит", "Бухгалтерский учёт", "Налоги", "Стандарты", "Аналитика", "Excel"], "salary_junior": "60 000 - 85 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "tax_consultant", "title": "Налоговый консультант", "skills": ["Налоговое право", "1С", "Excel", "Консультации", "Документооборот", "Аналитика"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "treasurer", "title": "Казначей", "skills": ["Управление ликвидностью", "Excel", "Банковские операции", "Прогнозирование", "Аналитика", "1С"], "salary_junior": "60 000 - 85 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "cfo", "title": "Финансовый директор (CFO)", "skills": ["Финансовая стратегия", "Бюджетирование", "Управление", "Аналитика", "Риски", "Отчётность"], "salary_junior": "150 000 - 250 000 ₽", "salary_middle": "300 000 - 500 000 ₽"},
        {"id": "investment_analyst", "title": "Инвестиционный аналитик", "skills": ["Финансовый анализ", "Excel", "Оценка бизнеса", "Моделирование", "Рынки", "Презентации"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 220 000 ₽"},
        {"id": "credit_analyst", "title": "Кредитный аналитик", "skills": ["Кредитный анализ", "Excel", "Финансовый анализ", "Риски", "Отчётность", "SQL"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 160 000 ₽"},
    ]},
    "legal": {"name": "Юриспруденция", "roles": [
        {"id": "lawyer", "title": "Юрист", "skills": ["Гражданское право", "Договорное право", "Документооборот", "Судебная практика", "Консультации", "Аналитика"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "corporate_lawyer", "title": "Корпоративный юрист", "skills": ["Корпоративное право", "M&A", "Договоры", "Due Diligence", "Комплаенс", "Документооборот"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "ip_lawyer", "title": "Юрист по интеллектуальной собственности", "skills": ["Патентное право", "Авторское право", "Торговые марки", "Лицензии", "Документооборот", "Консультации"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "compliance_officer", "title": "Специалист по комплаенсу", "skills": ["Комплаенс", "Регулирование", "Аудит", "Политики", "Обучение", "Документооборот"], "salary_junior": "60 000 - 85 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "labor_lawyer", "title": "Юрист по трудовому праву", "skills": ["Трудовое право", "Кадровый учёт", "Судебная практика", "Консультации", "Документооборот", "Медиация"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
    ]},
    "logistics_and_supply_chain": {"name": "Логистика и цепочки поставок", "roles": [
        {"id": "logistics_manager", "title": "Логист-менеджер", "skills": ["Логистика", "Управление запасами", "1С", "Excel", "Переговоры", "Планирование"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "supply_chain_manager", "title": "Менеджер цепочек поставок", "skills": ["Supply Chain", "Планирование", "Excel", "ERP", "Аналитика", "Переговоры"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "warehouse_manager", "title": "Начальник склада", "skills": ["Складская логистика", "WMS", "Управление командой", "1С", "Инвентаризация", "Безопасность"], "salary_junior": "50 000 - 70 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "purchasing_manager", "title": "Менеджер по закупкам", "skills": ["Закупки", "Переговоры", "Excel", "1С", "Аналитика", "Контрактное право"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "customs_specialist", "title": "Специалист по таможенному оформлению", "skills": ["Таможенное право", "Декларирование", "ВЭД", "Документооборот", "1С", "Аналитика"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "transport_manager", "title": "Менеджер по транспорту", "skills": ["Транспортная логистика", "TMS", "Планирование", "Excel", "Переговоры", "Мониторинг"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
    ]},
    "engineering_and_manufacturing": {"name": "Инженерия и производство", "roles": [
        {"id": "mechanical_engineer", "title": "Инженер-механик", "skills": ["AutoCAD", "SolidWorks", "Чертёжное дело", "Материаловедение", "Технологии", "Контроль качества"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "electrical_engineer", "title": "Инженер-электрик", "skills": ["Электроснабжение", "AutoCAD Electrical", "ПУЭ", "Проектирование", "Монтаж", "Контроль качества"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "civil_engineer", "title": "Инженер-строитель", "skills": ["AutoCAD", "Revit", "Проектирование", "Сметы", "Строительные нормы", "Контроль качества"], "salary_junior": "55 000 - 85 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "quality_engineer", "title": "Инженер по качеству", "skills": ["Контроль качества", "ISO", "Статистика", "Аудит", "Документооборот", "Аналитика"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "process_engineer", "title": "Инженер-технолог", "skills": ["Технологии производства", "Оптимизация", "Lean", "Документооборот", "Аналитика", "Контроль качества"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "safety_engineer", "title": "Инженер по охране труда", "skills": ["Охрана труда", "Техносфера", "Документооборот", "Аудит", "Обучение", "Законодательство"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "automation_engineer", "title": "Инженер по автоматизации", "skills": ["PLC", "SCADA", "Python", "Автоматизация", "Электрика", "Документооборот"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "construction_manager", "title": "Прораб", "skills": ["Строительство", "Управление командой", "Документооборот", "Сметы", "Контроль качества", "Планирование"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
    ]},
    "telecom": {"name": "Телекоммуникации", "roles": [
        {"id": "telecom_engineer", "title": "Инженер телекоммуникаций", "skills": ["Сети", "Cisco", "Linux", "Мониторинг", "Протоколы", "Документооборот"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "network_admin", "title": "Сетевой администратор", "skills": ["Cisco", "Linux", "Routing", "Switching", "Мониторинг", "Документооборот"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "radio_engineer", "title": "Инженер радиосвязи", "skills": ["Радиосвязь", "Антенны", "Измерения", "Документооборот", "Протоколы", "Мониторинг"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "fiber_engineer", "title": "Инженер ВОЛС", "skills": ["Оптоволокно", "Сварка", "Измерения", "Проектирование", "Документооборот", "Монтаж"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "noc_engineer", "title": "NOC-инженер", "skills": ["Мониторинг", "Linux", "Сети", "Документооборот", "Troubleshooting", "Коммуникация"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
    ]},
    "healthcare": {"name": "Медицина и фармацевтика", "roles": [
        {"id": "pharmacist", "title": "Фармацевт", "skills": ["Фармакология", "Документооборот", "Консультации", "Учёт", "Контроль качества", "Знание препаратов"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 100 000 ₽"},
        {"id": "medical_rep", "title": "Медицинский представитель", "skills": ["Продажи", "Фармакология", "Презентации", "CRM", "Переговоры", "Документооборот"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "clinical_research", "title": "Специалист по клиническим исследованиям", "skills": ["Клинические исследования", "GCP", "Документооборот", "Аналитика", "Регулирование", "Статистика"], "salary_junior": "60 000 - 85 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "lab_technician", "title": "Лаборант", "skills": ["Лабораторная диагностика", "Оборудование", "Документооборот", "Контроль качества", "Аналитика", "Безопасность"], "salary_junior": "30 000 - 45 000 ₽", "salary_middle": "50 000 - 80 000 ₽"},
        {"id": "medical_writer", "title": "Медицинский писатель", "skills": ["Медицинские тексты", "Копирайтинг", "Документооборот", "Редактура", "Регулирование", "Аналитика"], "salary_junior": "45 000 - 70 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
    ]},
    "education": {"name": "Образование", "roles": [
        {"id": "teacher", "title": "Учитель", "skills": ["Педагогика", "Методика", "Планирование", "Коммуникация", "Оценка знаний", "Документооборот"], "salary_junior": "30 000 - 45 000 ₽", "salary_middle": "50 000 - 80 000 ₽"},
        {"id": "tutor", "title": "Репетитор", "skills": ["Педагогика", "Индивидуальный подход", "Планирование", "Коммуникация", "Мотивация", "Методика"], "salary_junior": "30 000 - 50 000 ₽", "salary_middle": "60 000 - 120 000 ₽"},
        {"id": "instructional_designer", "title": "Методист / Instructional Designer", "skills": ["Педагогика", "E-learning", "Контент", "Планирование", "Оценка", "Документооборот"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "training_coordinator", "title": "Координатор обучения", "skills": ["Организация", "Планирование", "Коммуникация", "Документооборот", "E-learning", "Координация"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 100 000 ₽"},
        {"id": "academic_admin", "title": "Администратор учебного заведения", "skills": ["Администрирование", "Документооборот", "Планирование", "Коммуникация", "Бюджетирование", "Управление"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
    ]},
    "customer_service": {"name": "Обслуживание клиентов", "roles": [
        {"id": "customer_support", "title": "Специалист службы поддержки", "skills": ["Коммуникация", "Решение проблем", "CRM", "Документооборот", "Эмпатия", "Терпение"], "salary_junior": "30 000 - 45 000 ₽", "salary_middle": "50 000 - 80 000 ₽"},
        {"id": "customer_success", "title": "Customer Success Manager", "skills": ["Клиентоориентированность", "CRM", "Коммуникация", "Аналитика", "Онбординг", "Удержание"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "helpdesk_specialist", "title": "Специалист Helpdesk", "skills": ["IT-поддержка", "Тикет-системы", "Коммуникация", "Документооборот", "Troubleshooting", "Базы знаний"], "salary_junior": "35 000 - 50 000 ₽", "salary_middle": "60 000 - 90 000 ₽"},
        {"id": "call_center_agent", "title": "Оператор колл-центра", "skills": ["Коммуникация", "Стрессоустойчивость", "CRM", "Скорость", "Документооборот", "Клиентоориентированность"], "salary_junior": "25 000 - 40 000 ₽", "salary_middle": "45 000 - 70 000 ₽"},
    ]},
    "retail": {"name": "Ритейл и торговля", "roles": [
        {"id": "retail_manager", "title": "Менеджер магазина", "skills": ["Управление командой", "Продажи", "Инвентаризация", "Кассовый учёт", "Документооборот", "Клиентоориентированность"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "retail_buyer", "title": "Байер", "skills": ["Закупки", "Аналитика", "Переговоры", "Тренды", "Excel", "Документооборот"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "visual_merchandiser", "title": "Визуальный мерчандайзер", "skills": ["Визуальный маркетинг", "Дизайн", "Тренды", "Организация", "Креатив", "Коммуникация"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "e_commerce_manager", "title": "Менеджер интернет-магазина", "skills": ["E-commerce", "CMS", "Аналитика", "SEO", "Контент", "Документооборот"], "salary_junior": "45 000 - 70 000 ₽", "salary_middle": "80 000 - 140 000 ₽"},
        {"id": "inventory_manager", "title": "Менеджер по инвентаризации", "skills": ["Инвентаризация", "1С", "Excel", "Аналитика", "Документооборот", "Планирование"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 110 000 ₽"},
    ]},
    "real_estate": {"name": "Недвижимость", "roles": [
        {"id": "real_estate_agent", "title": "Риелтор", "skills": ["Продажи", "Переговоры", "Документооборот", "Рынок недвижимости", "CRM", "Презентации"], "salary_junior": "40 000 - 70 000 ₽", "salary_middle": "80 000 - 200 000 ₽"},
        {"id": "property_manager", "title": "Управляющий недвижимостью", "skills": ["Управление", "Документооборот", "Ремонт", "Бюджетирование", "Коммуникация", "Юридические вопросы"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 140 000 ₽"},
        {"id": "real_estate_analyst", "title": "Аналитик недвижимости", "skills": ["Аналитика", "Excel", "Оценка", "Рынок", "Презентации", "SQL"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "appraiser", "title": "Оценщик недвижимости", "skills": ["Оценка", "Документооборот", "Рынок", "Аналитика", "Законодательство", "Excel"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
    ]},
    "media_and_entertainment": {"name": "Медиа и развлечения", "roles": [
        {"id": "journalist", "title": "Журналист", "skills": ["Копирайтинг", "Редактура", "Интервью", "Исследования", "SEO", "Документооборот"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "65 000 - 110 000 ₽"},
        {"id": "editor", "title": "Редактор", "skills": ["Редактура", "Копирайтинг", "Контент-план", "SEO", "Документооборот", "Коммуникация"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "video_editor", "title": "Видеомонтажёр", "skills": ["Premiere Pro", "DaVinci Resolve", "After Effects", "Цветокоррекция", "Звук", "Креатив"], "salary_junior": "40 000 - 65 000 ₽", "salary_middle": "75 000 - 130 000 ₽"},
        {"id": "sound_engineer", "title": "Звукорежиссёр", "skills": ["Pro Tools", "Микширование", "Звуковой дизайн", "Мастеринг", "Запись", "Креатив"], "salary_junior": "40 000 - 65 000 ₽", "salary_middle": "75 000 - 130 000 ₽"},
        {"id": "producer", "title": "Продюсер", "skills": ["Управление проектами", "Бюджетирование", "Переговоры", "Коммуникация", "Планирование", "Креатив"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "120 000 - 200 000 ₽"},
        {"id": "photographer", "title": "Фотограф", "skills": ["Фотография", "Photoshop", "Lightroom", "Композиция", "Освещение", "Креатив"], "salary_junior": "30 000 - 50 000 ₽", "salary_middle": "60 000 - 110 000 ₽"},
        {"id": "copywriter", "title": "Копирайтер", "skills": ["Копирайтинг", "SEO", "Редактура", "Исследования", "Креатив", "Документооборот"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "65 000 - 110 000 ₽"},
        {"id": "translator", "title": "Переводчик", "skills": ["Перевод", "Редактура", "Специализация", "Документооборот", "Культурная адаптация", "Коммуникация"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "65 000 - 110 000 ₽"},
    ]},
    "construction": {"name": "Строительство", "roles": [
        {"id": "estimator", "title": "Сметчик", "skills": ["Сметное дело", "1С", "Excel", "Чтение чертежей", "Документооборот", "Нормативы"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "foreman", "title": "Мастер участка", "skills": ["Строительство", "Управление командой", "Документооборот", "Контроль качества", "Безопасность", "Планирование"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 160 000 ₽"},
        {"id": "bim_specialist", "title": "BIM-специалист", "skills": ["Revit", "BIM", "AutoCAD", "Навигация", "Документооборот", "Координация"], "salary_junior": "60 000 - 85 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "architect", "title": "Архитектор", "skills": ["Архитектура", "AutoCAD", "Revit", "Проектирование", "Креатив", "Документооборот"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "land_surveyor", "title": "Геодезист", "skills": ["Геодезия", "Приборы", "Автокад", "Документооборот", "Точность", "Вычисления"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
    ]},
    "agriculture": {"name": "Сельское хозяйство", "roles": [
        {"id": "agronomist", "title": "Агроном", "skills": ["Агрономия", "Почвоведение", "Защита растений", "Планирование", "Документооборот", "Аналитика"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 100 000 ₽"},
        {"id": "vet", "title": "Ветеринар", "skills": ["Ветеринария", "Диагностика", "Хирургия", "Документооборот", "Лекарства", "Коммуникация"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "65 000 - 110 000 ₽"},
        {"id": "farm_manager", "title": "Управляющий фермой", "skills": ["Управление", "Планирование", "Бюджетирование", "Документооборот", "Технологии", "Коммуникация"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "food_technologist", "title": "Технолог пищевых производств", "skills": ["Технология", "Контроль качества", "Документооборот", "Стандарты", "Аналитика", "Безопасность"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
    ]},
    "transport": {"name": "Транспорт", "roles": [
        {"id": "driver", "title": "Водитель", "skills": ["Вождение", "Навигация", "Документооборот", "Безопасность", "Техобслуживание", "Коммуникация"], "salary_junior": "35 000 - 50 000 ₽", "salary_middle": "55 000 - 90 000 ₽"},
        {"id": "fleet_manager", "title": "Менеджер автопарка", "skills": ["Логистика", "Управление", "Документооборот", "Мониторинг", "Бюджетирование", "Аналитика"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "dispatcher", "title": "Диспетчер", "skills": ["Координация", "Коммуникация", "Документооборот", "Стрессоустойчивость", "Планирование", "Мониторинг"], "salary_junior": "30 000 - 45 000 ₽", "salary_middle": "50 000 - 75 000 ₽"},
    ]},
    "cleaning_and_services": {"name": "Клининг и услуги", "roles": [
        {"id": "cleaner", "title": "Уборщик / Клинер", "skills": ["Уборка", "Чистящие средства", "Оборудование", "Внимание к деталям", "Физическая выносливость", "Надёжность"], "salary_junior": "25 000 - 35 000 ₽", "salary_middle": "35 000 - 50 000 ₽"},
        {"id": "cleaning_supervisor", "title": "Супервайзер клининга", "skills": ["Управление командой", "Планирование", "Контроль качества", "Документооборот", "Коммуникация", "Обучение"], "salary_junior": "40 000 - 55 000 ₽", "salary_middle": "60 000 - 90 000 ₽"},
        {"id": "pest_control", "title": "Специалист по дезинсекции", "skills": ["Дезинсекция", "Безопасность", "Оборудование", "Документооборот", "Химия", "Коммуникация"], "salary_junior": "30 000 - 45 000 ₽", "salary_middle": "50 000 - 80 000 ₽"},
        {"id": "facility_manager", "title": "Управляющий зданием", "skills": ["Управление", "Ремонт", "Бюджетирование", "Документооборот", "Коммуникация", "Безопасность"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 160 000 ₽"},
    ]},
    "security": {"name": "Безопасность", "roles": [
        {"id": "security_guard", "title": "Охранник", "skills": ["Наблюдательность", "Физическая подготовка", "Коммуникация", "Документооборот", "Стрессоустойчивость", "Законодательство"], "salary_junior": "25 000 - 40 000 ₽", "salary_middle": "40 000 - 60 000 ₽"},
        {"id": "security_manager", "title": "Менеджер по безопасности", "skills": ["Управление", "Риски", "Документооборот", "Законодательство", "Аудит", "Коммуникация"], "salary_junior": "60 000 - 85 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "fire_safety", "title": "Специалист по пожарной безопасности", "skills": ["Пожарная безопасность", "Документооборот", "Аудит", "Обучение", "Законодательство", "Коммуникация"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 110 000 ₽"},
        {"id": "investigator", "title": "Частный детектив", "skills": ["Наблюдение", "Аналитика", "Документооборот", "Законодательство", "Коммуникация", "Техника"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
    ]},
    "hospitality": {"name": "Гостиничный бизнес и рестораны", "roles": [
        {"id": "hotel_manager", "title": "Управляющий отелем", "skills": ["Управление", "Клиентоориентированность", "Бюджетирование", "Документооборот", "Коммуникация", "Маркетинг"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
        {"id": "receptionist", "title": "Администратор ресепшн", "skills": ["Коммуникация", "Клиентоориентированность", "Документооборот", "Языки", "Организация", "Стрессоустойчивость"], "salary_junior": "30 000 - 45 000 ₽", "salary_middle": "45 000 - 70 000 ₽"},
        {"id": "restaurant_manager", "title": "Управляющий рестораном", "skills": ["Управление", "Клиентоориентированность", "Бюджетирование", "Документооборот", "Кухня", "Коммуникация"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 160 000 ₽"},
        {"id": "sommelier", "title": "Сомелье", "skills": ["Вино", "Дегустация", "Коммуникация", "Сервис", "Клиентоориентированность", "Документооборот"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "chef", "title": "Шеф-повар", "skills": ["Кулинария", "Управление", "Креатив", "Документооборот", "Контроль качества", "Коммуникация"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "110 000 - 200 000 ₽"},
        {"id": "waiter", "title": "Официант", "skills": ["Сервис", "Коммуникация", "Клиентоориентированность", "Стрессоустойчивость", "Работа в команде", "Физическая выносливость"], "salary_junior": "25 000 - 40 000 ₽", "salary_middle": "40 000 - 65 000 ₽"},
        {"id": "cook", "title": "Повар", "skills": ["Кулинария", "Рецепты", "Гигиена", "Работа в команде", "Физическая выносливость", "Креатив"], "salary_junior": "30 000 - 45 000 ₽", "salary_middle": "50 000 - 80 000 ₽"},
        {"id": "barista", "title": "Бариста", "skills": ["Кофе", "Сервис", "Коммуникация", "Клиентоориентированность", "Работа с оборудованием", "Креатив"], "salary_junior": "25 000 - 40 000 ₽", "salary_middle": "40 000 - 60 000 ₽"},
    ]},
    "energy": {"name": "Энергетика", "roles": [
        {"id": "power_engineer", "title": "Инженер-энергетик", "skills": ["Электроснабжение", "Проектирование", "Документооборот", "Монтаж", "Контроль качества", "Безопасность"], "salary_junior": "55 000 - 80 000 ₽", "salary_middle": "100 000 - 170 000 ₽"},
        {"id": "energy_auditor", "title": "Энергоаудитор", "skills": ["Энергоаудит", "Измерения", "Аналитика", "Документооборот", "Энергосбережение", "Отчётность"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "solar_engineer", "title": "Инженер солнечной энергетики", "skills": ["Солнечные панели", "Проектирование", "Электротехника", "Документооборот", "Монтаж", "Аналитика"], "salary_junior": "60 000 - 90 000 ₽", "salary_middle": "110 000 - 180 000 ₽"},
    ]},
    "science_and_research": {"name": "Наука и исследования", "roles": [
        {"id": "researcher", "title": "Научный сотрудник", "skills": ["Исследования", "Аналитика", "Публикации", "Статистика", "Документооборот", "Презентации"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "lab_researcher", "title": "Лабораторный исследователь", "skills": ["Лабораторные методы", "Аналитика", "Документооборот", "Оборудование", "Безопасность", "Публикации"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "bioinformatician", "title": "Биоинформатик", "skills": ["Python", "R", "Биология", "Статистика", "Геномика", "Аналитика"], "salary_junior": "70 000 - 100 000 ₽", "salary_middle": "130 000 - 210 000 ₽"},
        {"id": "chemist", "title": "Химик-аналитик", "skills": ["Химия", "Аналитика", "Оборудование", "Документооборот", "Безопасность", "Публикации"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "physicist", "title": "Физик-исследователь", "skills": ["Физика", "Математика", "Моделирование", "Публикации", "Документооборот", "Аналитика"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
    ]},
    "social_work": {"name": "Социальная работа", "roles": [
        {"id": "social_worker", "title": "Социальный работник", "skills": ["Коммуникация", "Эмпатия", "Документооборот", "Законодательство", "Кризис-менеджмент", "Организация"], "salary_junior": "25 000 - 40 000 ₽", "salary_middle": "45 000 - 70 000 ₽"},
        {"id": "psychologist", "title": "Психолог", "skills": ["Консультирование", "Диагностика", "Терапия", "Документооборот", "Эмпатия", "Коммуникация"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "65 000 - 110 000 ₽"},
        {"id": "case_manager", "title": "Кейс-менеджер", "skills": ["Координация", "Документооборот", "Коммуникация", "Организация", "Аналитика", "Законодательство"], "salary_junior": "35 000 - 50 000 ₽", "salary_middle": "55 000 - 85 000 ₽"},
    ]},
    "non_profit": {"name": "НКО и благотворительность", "roles": [
        {"id": "ngo_manager", "title": "Менеджер НКО", "skills": ["Управление проектами", "Гранты", "Коммуникация", "Документооборот", "Бюджетирование", "Фандрайзинг"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "fundraiser", "title": "Фандрайзер", "skills": ["Фандрайзинг", "Коммуникация", "Презентации", "Документооборот", "CRM", "Аналитика"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "grant_writer", "title": "Специалист по грантам", "skills": ["Гранты", "Документооборот", "Исследования", "Копирайтинг", "Аналитика", "Планирование"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "75 000 - 120 000 ₽"},
    ]},
    "sport": {"name": "Спорт и фитнес", "roles": [
        {"id": "fitness_trainer", "title": "Фитнес-тренер", "skills": ["Фитнес", "Анатомия", "Коммуникация", "Мотивация", "Планирование", "Безопасность"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 110 000 ₽"},
        {"id": "sports_coach", "title": "Спортивный тренер", "skills": ["Тренировки", "Физиология", "Планирование", "Коммуникация", "Мотивация", "Аналитика"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 110 000 ₽"},
        {"id": "sports_manager", "title": "Спортивный менеджер", "skills": ["Управление", "Организация", "Маркетинг", "Документооборот", "Коммуникация", "Бюджетирование"], "salary_junior": "50 000 - 75 000 ₽", "salary_middle": "90 000 - 150 000 ₽"},
        {"id": "sports_analyst", "title": "Спортивный аналитик", "skills": ["Аналитика", "Статистика", "Excel", "Спорт", "Данные", "Визуализация"], "salary_junior": "45 000 - 70 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
    ]},
    "beauty": {"name": "Бьюти-индустрия", "roles": [
        {"id": "hairdresser", "title": "Парикмахер", "skills": ["Стрижки", "Окрашивание", "Укладка", "Коммуникация", "Клиентоориентированность", "Креатив"], "salary_junior": "30 000 - 50 000 ₽", "salary_middle": "55 000 - 100 000 ₽"},
        {"id": "makeup_artist", "title": "Визажист", "skills": ["Макияж", "Косметика", "Креатив", "Коммуникация", "Клиентоориентированность", "Тренды"], "salary_junior": "30 000 - 50 000 ₽", "salary_middle": "55 000 - 100 000 ₽"},
        {"id": "nail_technician", "title": "Мастер маникюра", "skills": ["Маникюр", "Дизайн", "Гигиена", "Коммуникация", "Клиентоориентированность", "Тренды"], "salary_junior": "25 000 - 45 000 ₽", "salary_middle": "50 000 - 90 000 ₽"},
        {"id": "cosmetologist", "title": "Косметолог", "skills": ["Косметология", "Дерматология", "Процедуры", "Коммуникация", "Безопасность", "Документооборот"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 120 000 ₽"},
        {"id": "massage_therapist", "title": "Массажист", "skills": ["Массаж", "Анатомия", "Физиология", "Коммуникация", "Клиентоориентированность", "Безопасность"], "salary_junior": "30 000 - 50 000 ₽", "salary_middle": "55 000 - 90 000 ₽"},
    ]},
    "crafts": {"name": "Ремёсла и производство", "roles": [
        {"id": "welder", "title": "Сварщик", "skills": ["Сварка", "Чертёжное дело", "Безопасность", "Материаловедение", "Оборудование", "Точность"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 110 000 ₽"},
        {"id": "electrician", "title": "Электрик", "skills": ["Электромонтаж", "ПУЭ", "Безопасность", "Оборудование", "Документооборот", "Диагностика"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 100 000 ₽"},
        {"id": "plumber", "title": "Сантехник", "skills": ["Сантехника", "Монтаж", "Диагностика", "Оборудование", "Безопасность", "Документооборот"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 100 000 ₽"},
        {"id": "carpenter", "title": "Плотник", "skills": ["Столярное дело", "Инструменты", "Чертёжное дело", "Материаловедение", "Точность", "Безопасность"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 100 000 ₽"},
        {"id": "painter", "title": "Маляр", "skills": ["Покраска", "Подготовка поверхностей", "Материалы", "Инструменты", "Точность", "Безопасность"], "salary_junior": "30 000 - 50 000 ₽", "salary_middle": "55 000 - 85 000 ₽"},
    ]},
    "auto": {"name": "Автомобильная отрасль", "roles": [
        {"id": "auto_mechanic", "title": "Автомеханик", "skills": ["Ремонт", "Диагностика", "Оборудование", "Документооборот", "Безопасность", "Запчасти"], "salary_junior": "35 000 - 55 000 ₽", "salary_middle": "60 000 - 100 000 ₽"},
        {"id": "auto_electrician", "title": "Автоэлектрик", "skills": ["Электрика", "Диагностика", "Оборудование", "Электроника", "Документооборот", "Безопасность"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 110 000 ₽"},
        {"id": "auto_diagnostics", "title": "Диагност автомобилей", "skills": ["Диагностика", "Оборудование", "Электроника", "Аналитика", "Документооборот", "Коммуникация"], "salary_junior": "45 000 - 65 000 ₽", "salary_middle": "80 000 - 130 000 ₽"},
        {"id": "auto_parts_manager", "title": "Менеджер автозапчастей", "skills": ["Запчасти", "1С", "Инвентаризация", "Продажи", "Документооборот", "Коммуникация"], "salary_junior": "40 000 - 60 000 ₽", "salary_middle": "70 000 - 110 000 ₽"},
        {"id": "car_salesman", "title": "Менеджер по продажам автомобилей", "skills": ["Продажи", "Переговоры", "Автомобили", "CRM", "Коммуникация", "Документооборот"], "salary_junior": "45 000 - 70 000 ₽", "salary_middle": "80 000 - 150 000 ₽"},
    ]},
}

# ============================================================================
# ШАБЛОНЫ СЦЕНАРИЕВ — универсальные вопросы для каждой категории
# ============================================================================
IT_J = [
    {"q": "Что такое REST API?", "o": [
        {"text": "Язык программирования", "score": 0}, {"text": "Протокол обмена данными клиент-сервер", "score": 15},
        {"text": "База данных", "score": 0}, {"text": "Архитектурный стиль для веб-сервисов с HTTP-методами", "score": 20},
        {"text": "Фреймворк для фронтенда", "score": 0},
    ]},
    {"q": "Как отладить баг у некоторых пользователей?", "o": [
        {"text": "Воспроизведу у себя", "score": 5}, {"text": "Посмотрю логи и соберу инфо", "score": 15},
        {"text": "Скажу что не могу без воспроизведения", "score": 0}, {"text": "Проанализирую логи, метрики, окружение, создам тестовый сценарий", "score": 20},
        {"text": "Попрошу коллег", "score": 2},
    ]},
    {"q": "Что такое Git?", "o": [
        {"text": "Текстовый редактор", "score": 0}, {"text": "Система контроля версий для отслеживания изменений", "score": 18},
        {"text": "Язык программирования", "score": 0}, {"text": "Инструмент совместной работы с историей изменений и ветвлением", "score": 20},
        {"text": "Хостинг для сайтов", "score": 0},
    ]},
    {"q": "Как изучаешь новую технологию?", "o": [
        {"text": "Документация + маленький проект", "score": 15}, {"text": "Видео на YouTube", "score": 5},
        {"text": "Подожду пока научат", "score": 0}, {"text": "Документация, pet-проект, примеры, сообщество", "score": 20},
        {"text": "Книга", "score": 8},
    ]},
    {"q": "SQL vs NoSQL?", "o": [
        {"text": "Одно и то же", "score": 0}, {"text": "SQL — таблицы, NoSQL — документы/ключ-значение", "score": 18},
        {"text": "SQL быстрее", "score": 3}, {"text": "SQL — реляционные БД, NoSQL — нереляционные для разных задач", "score": 20},
        {"text": "NoSQL устарел", "score": 0},
    ]},
]
IT_M = [
    {"q": "Как проектируешь архитектуру сервиса?", "o": [
        {"text": "Пишу код и смотрю", "score": 0}, {"text": "Рисую схему, компоненты, API, БД", "score": 15},
        {"text": "Копирую из прошлого проекта", "score": 5}, {"text": "Анализирую требования, паттерны, API, БД, масштабируемость, мониторинг", "score": 20},
        {"text": "Микросервисы для всего", "score": 5},
    ]},
    {"q": "Как обеспечиваешь качество кода?", "o": [
        {"text": "Пишу аккуратно", "score": 3}, {"text": "Code review, линтеры, тесты", "score": 15},
        {"text": "Доверяю опытным", "score": 2}, {"text": "Code review, автотесты, линтеры, CI/CD, стандарты", "score": 20},
        {"text": "Тестирую перед релизом", "score": 8},
    ]},
    {"q": "Как оптимизируешь медленный SQL-запрос?", "o": [
        {"text": "Добавлю индексы", "score": 10}, {"text": "Перепишу запрос", "score": 8},
        {"text": "Explain plan, индексы, оптимизация, кэширование", "score": 20},
        {"text": "Мощнее сервер", "score": 0}, {"text": "Разобью таблицу", "score": 5},
    ]},
    {"q": "Как обрабатываешь ошибки в продакшене?", "o": [
        {"text": "Try-catch и логи", "score": 12}, {"text": "Игнорирую не критичные", "score": 0},
        {"text": "Централизованный логгинг, алертинг, graceful degradation, retry", "score": 20},
        {"text": "Try-catch везде", "score": 8}, {"text": "Жду жалоб", "score": 0},
    ]},
    {"q": "Микросервисы или монолит?", "o": [
        {"text": "Микросервисы всегда", "score": 0}, {"text": "Зависит от проекта и команды", "score": 12},
        {"text": "Монолит проще, микросервисы для больших команд", "score": 15},
        {"text": "Анализирую домен, команду, масштаб, ops-зрелость", "score": 20},
        {"text": "Только для крупных компаний", "score": 5},
    ]},
    {"q": "Как подходишь к безопасности?", "o": [
        {"text": "HTTPS", "score": 5}, {"text": "Валидация, prepared statements", "score": 12},
        {"text": "Security audit, auth, шифрование, OWASP Top 10", "score": 20},
        {"text": "Доверяю фреймворку", "score": 3}, {"text": "Проверяю после релиза", "score": 2},
    ]},
    {"q": "Как управляешь техдолгом?", "o": [
        {"text": "Рефакторю когда есть время", "score": 8}, {"text": "В бэклог", "score": 5},
        {"text": "20% спринта, приоритизация по риску, документация", "score": 20},
        {"text": "Игнорирую", "score": 0}, {"text": "Рефакторю всё", "score": 3},
    ]},
]
DESIGN_J = [
    {"q": "Что такое дизайн-система?", "o": [
        {"text": "Набор иконок", "score": 0}, {"text": "Набор UI компонентов", "score": 10},
        {"text": "Единая система компонентов, стилей, паттернов для согласованного продукта", "score": 20},
        {"text": "Библиотека шрифтов", "score": 0}, {"text": "Стиль оформления", "score": 5},
    ]},
    {"q": "Как выбираешь цвета?", "o": [
        {"text": "Понравившиеся", "score": 0}, {"text": "Из гайдлайнов", "score": 10},
        {"text": "Контрастность, доступность, брендинг, психология, тестирование", "score": 20},
        {"text": "Копирую у конкурентов", "score": 2}, {"text": "Рандомно", "score": 0},
    ]},
    {"q": "Что такое user research?", "o": [
        {"text": "Поиск пользователей в интернете", "score": 0},
        {"text": "Изучение потребностей через интервью, опросы, тестирования", "score": 20},
        {"text": "Анализ конкурентов", "score": 5}, {"text": "Сбор статистики", "score": 8}, {"text": "Дизайн для пользователей", "score": 3},
    ]},
    {"q": "Как делаешь прототип?", "o": [
        {"text": "На бумаге", "score": 5}, {"text": "В Figma с интерактивностью", "score": 12},
        {"text": "Скетчи → wireframes → интерактивный прототип", "score": 20},
        {"text": "Сразу в коде", "score": 3}, {"text": "Прошу разработчика", "score": 0},
    ]},
    {"q": "Как получаешь фидбек по дизайну?", "o": [
        {"text": "Коллегам", "score": 8}, {"text": "Юзабилити-тестирование, фидбек стейкхолдеров", "score": 20},
        {"text": "Жду после релиза", "score": 0}, {"text": "У начальника", "score": 5}, {"text": "A/B тест", "score": 12},
    ]},
]
DESIGN_M = [
    {"q": "Как проектируешь дизайн-систему с нуля?", "o": [
        {"text": "В один файл", "score": 5}, {"text": "Дизайн-токены, библиотека, guidelines", "score": 20},
        {"text": "Копирую Material", "score": 8}, {"text": "Набор стилей", "score": 3}, {"text": "Как хотят", "score": 0},
    ]},
    {"q": "Баланс эстетики и usability?", "o": [
        {"text": "Красота", "score": 0}, {"text": "Usability", "score": 5},
        {"text": "Usability основа, эстетика усиливает, тестирую", "score": 20},
        {"text": "Компромисс", "score": 10}, {"text": "Тренды", "score": 3},
    ]},
    {"q": "Как работаешь с разработчиками?", "o": [
        {"text": "Отправляю макеты", "score": 3}, {"text": "Спецификации", "score": 8},
        {"text": "Дизайн-ревью, спецификации, обсуждение ограничений", "score": 20},
        {"text": "Рисую и забываю", "score": 0}, {"text": "Делаю сам", "score": 5},
    ]},
    {"q": "Как измеряешь успех дизайна?", "o": [
        {"text": "Нравится мне", "score": 0}, {"text": "Конверсия, время, ошибки, NPS", "score": 18},
        {"text": "Фидбек команды", "score": 5}, {"text": "Бизнес-метрики, A/B тесты, qualitative feedback", "score": 20},
        {"text": "Лайки", "score": 0},
    ]},
    {"q": "Как адаптируешь для людей с ОВЗ?", "o": [
        {"text": "Крупный шрифт", "score": 5}, {"text": "WCAG: контраст, alt, клавиатура, скринридеры", "score": 20},
        {"text": "Не думаю", "score": 0}, {"text": "Тёмная тема", "score": 3}, {"text": "Спрашиваю", "score": 8},
    ]},
]
DATA_J = [
    {"q": "Как проверяешь качество данных?", "o": [
        {"text": "Первые строки", "score": 3}, {"text": "Пропуски, дубликаты, аномалии", "score": 15},
        {"text": "Сразу анализ", "score": 0}, {"text": "Exploratory analysis, полнота, консистентность", "score": 20},
        {"text": "Доверяю источнику", "score": 0},
    ]},
    {"q": "Среднее vs медиана?", "o": [
        {"text": "Одно и то же", "score": 0}, {"text": "Среднее = сумма/n, медиана = середина", "score": 18},
        {"text": "Медиана больше", "score": 0}, {"text": "Среднее чувствительно к выбросам, медиана устойчива", "score": 20},
        {"text": "Не знаю", "score": 0},
    ]},
    {"q": "Как визуализируешь для нетехнической аудитории?", "o": [
        {"text": "Сложные графики", "score": 0}, {"text": "Простые диаграммы с пояснениями", "score": 12},
        {"text": "Простые визуализации, контекст, инсайты", "score": 20},
        {"text": "Таблицы", "score": 3}, {"text": "Сырые данные", "score": 0},
    ]},
    {"q": "Что такое A/B тест?", "o": [
        {"text": "Сравнение двух версий", "score": 18}, {"text": "Тестирование багов", "score": 0},
        {"text": "Сравнение сайтов", "score": 5}, {"text": "Сравнение с контрольной группой для стат. значимости", "score": 20},
        {"text": "Опрос", "score": 3},
    ]},
    {"q": "Как работаешь с SQL?", "o": [
        {"text": "Простые SELECT", "score": 5}, {"text": "JOIN, GROUP BY, подзапросы", "score": 15},
        {"text": "Окна, CTE, оптимизация", "score": 20}, {"text": "ORM", "score": 8}, {"text": "Не использую", "score": 0},
    ]},
]
DATA_M = [
    {"q": "Как выбираешь метрики продукта?", "o": [
        {"text": "Стандартные", "score": 5}, {"text": "Цели бизнеса, North Star, поддерживающие", "score": 20},
        {"text": "У руководства", "score": 3}, {"text": "У конкурентов", "score": 3}, {"text": "Что проще", "score": 0},
    ]},
    {"q": "Корреляция vs причинность?", "o": [
        {"text": "Одно и то же", "score": 0}, {"text": "Корреляция — связь, причинность — вызывает", "score": 15},
        {"text": "Корреляция ≠ причинность, нужны эксперименты", "score": 20},
        {"text": "Корреляция слабее", "score": 5}, {"text": "Не различаю", "score": 0},
    ]},
    {"q": "Как работаешь с missing data?", "o": [
        {"text": "Удаляю", "score": 5}, {"text": "Заполняю средним", "score": 8},
        {"text": "Анализирую паттерн, imputation, missing как категория", "score": 20},
        {"text": "Игнорирую", "score": 0}, {"text": "Нулями", "score": 3},
    ]},
    {"q": "Как создаёшь дашборд для руководства?", "o": [
        {"text": "Все метрики", "score": 0}, {"text": "Ключевые, визуализация, контекст", "score": 18},
        {"text": "Красивый дизайн", "score": 5}, {"text": "Аудитория, 5-7 метрик, drill-down", "score": 20},
        {"text": "Шаблон", "score": 3},
    ]},
    {"q": "Как оцениваешь стат. значимость?", "o": [
        {"text": "p-value", "score": 10}, {"text": "t-тест", "score": 12},
        {"text": "Подходящий тест, предпосылки, p-value + CI", "score": 20},
        {"text": "Размер выборки", "score": 5}, {"text": "Не проверяю", "score": 0},
    ]},
]
SALES_J = [
    {"q": "Как определяешь ЦА?", "o": [
        {"text": "Все", "score": 0}, {"text": "Демография, интересы, боли, персоны", "score": 20},
        {"text": "У коллег", "score": 3}, {"text": "У конкурентов", "score": 8}, {"text": "Проб и ошибок", "score": 5},
    ]},
    {"q": "Что такое воронка продаж?", "o": [
        {"text": "Процесс от привлечения до покупки", "score": 15}, {"text": "Список клиентов", "score": 0},
        {"text": "Этапы: awareness → interest → decision → action", "score": 20},
        {"text": "Рекламная кампания", "score": 0}, {"text": "План продаж", "score": 3},
    ]},
    {"q": "Возражение 'дорого'?", "o": [
        {"text": "Скидка", "score": 3}, {"text": "Качество стоит денег", "score": 8},
        {"text": "Реальная причина, ценность, ROI, альтернативы", "score": 20},
        {"text": "Заканчиваю", "score": 0}, {"text": "Рассрочка", "score": 10},
    ]},
    {"q": "Как измеряешь эффективность кампании?", "o": [
        {"text": "Лайки", "score": 0}, {"text": "CTR, конверсия, CPA, ROI, LTV", "score": 20},
        {"text": "Продажи", "score": 10}, {"text": "У клиентов", "score": 5}, {"text": "Жду", "score": 0},
    ]},
    {"q": "Что такое контент-маркетинг?", "o": [
        {"text": "Статьи", "score": 5}, {"text": "Ценный контент для привлечения и удержания", "score": 20},
        {"text": "Реклама", "score": 0}, {"text": "Посты в соцсетях", "score": 5}, {"text": "Email", "score": 3},
    ]},
]
SALES_M = [
    {"q": "Как строишь digital-стратегию?", "o": [
        {"text": "Реклама везде", "score": 0}, {"text": "Цели, аудитория, каналы, бюджет, KPI, тесты", "score": 20},
        {"text": "Копирую", "score": 3}, {"text": "Все каналы", "score": 5}, {"text": "Агентство", "score": 5},
    ]},
    {"q": "Как оптимизируешь воронку?", "o": [
        {"text": "Больше бюджета", "score": 0}, {"text": "Конверсии на этапах, узкие места, A/B тесты", "score": 20},
        {"text": "Тексты", "score": 5}, {"text": "Скидки", "score": 3}, {"text": "Больше продавцов", "score": 5},
    ]},
    {"q": "Как считаешь LTV?", "o": [
        {"text": "Средний чек × покупки", "score": 10}, {"text": "Чек × частота × удержание", "score": 18},
        {"text": "Общая выручка", "score": 0}, {"text": "Когорты, revenue per user × lifetime", "score": 20},
        {"text": "Не считаю", "score": 0},
    ]},
    {"q": "Как проводишь A/B тест?", "o": [
        {"text": "Меняю заголовок", "score": 5}, {"text": "Гипотеза, метрика, трафик, стат. значимость", "score": 20},
        {"text": "Два варианта", "score": 8}, {"text": "Фокус-группа", "score": 5}, {"text": "Интуитивно", "score": 0},
    ]},
    {"q": "Как работаешь с уходящими клиентами?", "o": [
        {"text": "Ничего", "score": 0}, {"text": "Exit-интервью, анализ, сегментация, win-back", "score": 20},
        {"text": "Уговариваю", "score": 5}, {"text": "Скидка", "score": 5}, {"text": "Анализ данных", "score": 10},
    ]},
]
MGMT_J = [
    {"q": "Как планируешь спринт?", "o": [
        {"text": "Все задачи", "score": 0}, {"text": "Приоритеты, сложность, capacity", "score": 18},
        {"text": "Равномерно", "score": 5}, {"text": "Цель спринта, приоритет, story points", "score": 20},
        {"text": "У команды", "score": 10},
    ]},
    {"q": "Как решаешь конфликт?", "o": [
        {"text": "Игнорирую", "score": 0}, {"text": "Обе стороны, компромисс", "score": 18},
        {"text": "Решаю сам", "score": 5}, {"text": "Встреча, открыто, win-win", "score": 20},
        {"text": "HR", "score": 3},
    ]},
    {"q": "Как отслеживаешь прогресс?", "o": [
        {"text": "Спрашиваю", "score": 5}, {"text": "Метрики, дашборды, стендапы, ретро", "score": 20},
        {"text": "Таск-трекер", "score": 10}, {"text": "Доверяю", "score": 3}, {"text": "В конце", "score": 5},
    ]},
    {"q": "Как ставишь цели?", "o": [
        {"text": "Говорю", "score": 0}, {"text": "SMART, контекст, согласование", "score": 18},
        {"text": "OKR", "score": 15}, {"text": "Бизнес-цели, OKR, вовлечение", "score": 20},
        {"text": "Дедлайны", "score": 5},
    ]},
    {"q": "Как управляешь рисками?", "o": [
        {"text": "Не думаю", "score": 0}, {"text": "Идентификация, вероятность, влияние, митигация", "score": 18},
        {"text": "По мере появления", "score": 5}, {"text": "Risk register, пересмотр, owners", "score": 20},
        {"text": "Делегирую", "score": 3},
    ]},
]
MGMT_M = [
    {"q": "Как принимаешь решение о найме?", "o": [
        {"text": "Резюме", "score": 0}, {"text": "Структурированное интервью, компетенции, референсы", "score": 18},
        {"text": "Рекомендация", "score": 5}, {"text": "Профиль, multi-stage, задание, fit", "score": 20},
        {"text": "Интуиция", "score": 3},
    ]},
    {"q": "Как управляешь изменениями?", "o": [
        {"text": "Объявляю", "score": 0}, {"text": "Vision, стейкхолдеры, переход, поддержка", "score": 20},
        {"text": "Постепенно", "score": 10}, {"text": "HR", "score": 3}, {"text": "Резко", "score": 5},
    ]},
    {"q": "Как измеряешь эффективность команды?", "o": [
        {"text": "Количество задач", "score": 0}, {"text": "Velocity, lead time, качество, удовлетворённость", "score": 18},
        {"text": "Сроки", "score": 5}, {"text": "Delivery, качество, team health, бизнес", "score": 20},
        {"text": "Отзывы", "score": 8},
    ]},
    {"q": "Как развиваешь команду?", "o": [
        {"text": "Курсы", "score": 5}, {"text": "1-on-1, цели, фидбек, возможности", "score": 20},
        {"text": "Сложные задачи", "score": 10}, {"text": "Саморазвитие", "score": 3}, {"text": "Тренинги", "score": 8},
    ]},
    {"q": "Как управляешь стейкхолдерами?", "o": [
        {"text": "Раз в месяц", "score": 3}, {"text": "Маппинг, ожидания, коммуникация, приоритеты", "score": 20},
        {"text": "Отвечаю", "score": 5}, {"text": "Игнорирую", "score": 0}, {"text": "Делегирую", "score": 5},
    ]},
]
HR_J = [
    {"q": "Как ищешь кандидатов?", "o": [
        {"text": "hh.ru", "score": 5}, {"text": "LinkedIn, Telegram, рефералки, сорсинг", "score": 15},
        {"text": "Профиль, Boolean search, outreach", "score": 20},
        {"text": "Жду", "score": 0}, {"text": "Агентство", "score": 8},
    ]},
    {"q": "Как проводишь собеседование?", "o": [
        {"text": "Из интернета", "score": 3}, {"text": "Подготовленные вопросы", "score": 10},
        {"text": "Структурированное по компетенциям с матрицей", "score": 20},
        {"text": "Свободно", "score": 5}, {"text": "Тестовое", "score": 8},
    ]},
    {"q": "Как адаптируешь нового?", "o": [
        {"text": "Показываю офис", "score": 3}, {"text": "План 30-60-90 дней, бадди, чеки", "score": 20},
        {"text": "Доступы и задача", "score": 0}, {"text": "Обучение", "score": 5}, {"text": "Представляю", "score": 8},
    ]},
    {"q": "Как работаешь с выгоранием?", "o": [
        {"text": "Не замечаю", "score": 0}, {"text": "1-on-1, причины, поддержка, нагрузка", "score": 20},
        {"text": "Отпуск", "score": 5}, {"text": "Нормально", "score": 0}, {"text": "Психолог", "score": 8},
    ]},
    {"q": "Как оцениваешь обучение?", "o": [
        {"text": "Понравилось", "score": 3}, {"text": "Тесты", "score": 10},
        {"text": "Изменение поведения, KPI, ROI", "score": 20},
        {"text": "Посещаемость", "score": 0}, {"text": "Отзывы", "score": 8},
    ]},
]
HR_M = [
    {"q": "Как строишь HR-стратегию?", "o": [
        {"text": "Копирую", "score": 0}, {"text": "Бизнес-стратегия, приоритеты, roadmap", "score": 20},
        {"text": "У сотрудников", "score": 5}, {"text": "Лучшие практики", "score": 10}, {"text": "По ситуации", "score": 3},
    ]},
    {"q": "Как измеряешь рекрутинг?", "o": [
        {"text": "Количество", "score": 3}, {"text": "Time to hire, cost, quality, source", "score": 18},
        {"text": "Скорость", "score": 5}, {"text": "Воронка, конверсии, retention", "score": 20},
        {"text": "Бюджет", "score": 5},
    ]},
    {"q": "Как управляешь employer branding?", "o": [
        {"text": "Вакансии", "score": 0}, {"text": "EVP, контент, advocacy, отзывы", "score": 20},
        {"text": "Ярмарки", "score": 8}, {"text": "Реклама", "score": 5}, {"text": "Ничего", "score": 0},
    ]},
    {"q": "Как проводишь оценку персонала?", "o": [
        {"text": "Раз в год", "score": 5}, {"text": "360, performance review, assessment", "score": 18},
        {"text": "KPI", "score": 8}, {"text": "Регулярный фидбек, review, развитие", "score": 20},
        {"text": "Руководители", "score": 3},
    ]},
    {"q": "Как работаешь с retention?", "o": [
        {"text": "Зарплата", "score": 5}, {"text": "Причины уходов, engagement, развитие", "score": 20},
        {"text": "Exit-интервью", "score": 8}, {"text": "Корпоративы", "score": 3}, {"text": "Ничего", "score": 0},
    ]},
]
FIN_J = [
    {"q": "Как проверяешь отчётность?", "o": [
        {"text": "Сверяю", "score": 5}, {"text": "Баланс, первичка, расхождения", "score": 15},
        {"text": "Reconciliation, проводки, выписки", "score": 20},
        {"text": "Программа", "score": 0}, {"text": "Коллеги", "score": 3},
    ]},
    {"q": "Дебиторская задолженность?", "o": [
        {"text": "Мы должны", "score": 0}, {"text": "Нам должны за товары/услуги", "score": 18},
        {"text": "Кредит", "score": 0}, {"text": "Задолженность клиентов за отгруженные товары", "score": 20},
        {"text": "Расходы", "score": 0},
    ]},
    {"q": "Как работаешь с НДС?", "o": [
        {"text": "20%", "score": 5}, {"text": "Книга покупок/продаж, вычет, декларация", "score": 18},
        {"text": "Делегирую", "score": 0}, {"text": "База, НДС к уплате, вычеты", "score": 20},
        {"text": "Не знаю", "score": 0},
    ]},
    {"q": "Как составляешь бюджет?", "o": [
        {"text": "Прошлый год", "score": 5}, {"text": "Исторические данные, прогноз", "score": 18},
        {"text": "У отделов", "score": 8}, {"text": "Запросы, тренды, реалистичный бюджет", "score": 20},
        {"text": "Как получается", "score": 0},
    ]},
    {"q": "Как работаешь с документами?", "o": [
        {"text": "Папки", "score": 3}, {"text": "Реестр, архив, сроки", "score": 15},
        {"text": "ЭДО, контроль сроков", "score": 20},
        {"text": "Секретарь", "score": 0}, {"text": "Компьютер", "score": 5},
    ]},
]
FIN_M = [
    {"q": "Как анализируешь фин. состояние?", "o": [
        {"text": "Прибыль", "score": 5}, {"text": "Ликвидность, рентабельность, долг, cash flow", "score": 18},
        {"text": "Коэффициенты", "score": 10}, {"text": "Горизонтальный, вертикальный, ratio, trend", "score": 20},
        {"text": "Аудитор", "score": 3},
    ]},
    {"q": "Как управляешь cash flow?", "o": [
        {"text": "Чтоб были", "score": 0}, {"text": "Прогноз поступлений/платежей, оборотный капитал", "score": 18},
        {"text": "Forecast, payment terms, working capital", "score": 20},
        {"text": "Кредит", "score": 5}, {"text": "Не планирую", "score": 0},
    ]},
    {"q": "Как оптимизируешь налоги?", "o": [
        {"text": "Вычеты", "score": 10}, {"text": "Законодательство, льготы, структура", "score": 20},
        {"text": "Консультант", "score": 5}, {"text": "Минимизирую", "score": 5}, {"text": "Ничего", "score": 0},
    ]},
    {"q": "Как проводишь аудит?", "o": [
        {"text": "Документы", "score": 5}, {"text": "Scope, evidence, findings, рекомендации", "score": 20},
        {"text": "Ошибки", "score": 8}, {"text": "Делегирую", "score": 0}, {"text": "Выборочно", "score": 10},
    ]},
    {"q": "Как управляешь рисками?", "o": [
        {"text": "Не думаю", "score": 0}, {"text": "Идентификация, оценка, хеджирование, страхование", "score": 20},
        {"text": "Резерв", "score": 10}, {"text": "Рынку", "score": 3}, {"text": "Интуиция", "score": 5},
    ]},
]
DEFAULT_J = [
    {"q": "Как решаешь незнакомую задачу?", "o": [
        {"text": "Помощь сразу", "score": 3}, {"text": "Гуглю, разбираюсь", "score": 12},
        {"text": "Документация, примеры, эксперты", "score": 20},
        {"text": "Откладываю", "score": 0}, {"text": "Как раньше", "score": 5},
    ]},
    {"q": "Как управляешь временем?", "o": [
        {"text": "Никак", "score": 0}, {"text": "Список задач", "score": 10},
        {"text": "Приоритизация, тайм-блокинг, трекер", "score": 20},
        {"text": "Важное первым", "score": 12}, {"text": "Указания", "score": 2},
    ]},
    {"q": "Как работаешь в команде?", "o": [
        {"text": "Свою часть", "score": 5}, {"text": "Общаюсь, помогаю", "score": 12},
        {"text": "Активно, делюсь, фидбек", "score": 20},
        {"text": "Один", "score": 0}, {"text": "Делегирую", "score": 3},
    ]},
    {"q": "Как реагируешь на критику?", "o": [
        {"text": "Обижаюсь", "score": 0}, {"text": "К сведению", "score": 10},
        {"text": "Анализирую, применяю", "score": 20},
        {"text": "Игнорирую", "score": 0}, {"text": "Спорю", "score": 3},
    ]},
    {"q": "Как развиваешь навыки?", "o": [
        {"text": "Когда есть время", "score": 5}, {"text": "Статьи, видео", "score": 10},
        {"text": "План, курсы, проекты, ментор", "score": 20},
        {"text": "Не развиваю", "score": 0}, {"text": "На работе", "score": 5},
    ]},
]
DEFAULT_M = [
    {"q": "Как принимаешь сложные решения?", "o": [
        {"text": "Интуиция", "score": 5}, {"text": "Информация, плюсы/минусы", "score": 15},
        {"text": "Данные, эксперты, риски", "score": 20},
        {"text": "Откладываю", "score": 0}, {"text": "Начальник", "score": 8},
    ]},
    {"q": "Как управляешь стрессом?", "o": [
        {"text": "Никак", "score": 0}, {"text": "Отдыхаю", "score": 8},
        {"text": "Техники, планирование, делегирование, баланс", "score": 20},
        {"text": "Больше работаю", "score": 3}, {"text": "Жалуюсь", "score": 0},
    ]},
    {"q": "Как ведёшь переговоры?", "o": [
        {"text": "Настаиваю", "score": 3}, {"text": "Компромисс", "score": 12},
        {"text": "Подготовка, цели, слушаю, win-win", "score": 20},
        {"text": "Уступаю", "score": 5}, {"text": "Избегаю", "score": 0},
    ]},
    {"q": "Как измеряешь рост?", "o": [
        {"text": "Зарплата", "score": 5}, {"text": "Должности", "score": 8},
        {"text": "Навыки, достижения, фидбек, влияние", "score": 20},
        {"text": "Не измеряю", "score": 0}, {"text": "Проекты", "score": 5},
    ]},
    {"q": "Как делишься знаниями?", "o": [
        {"text": "Никак", "score": 0}, {"text": "Когда спрашивают", "score": 8},
        {"text": "Воркшопы, документация, менторство", "score": 20},
        {"text": "Близким", "score": 5}, {"text": "По указанию", "score": 3},
    ]},
]

CATEGORY_MAP = {
    "it_and_development": (IT_J, IT_M),
    "design_and_creative": (DESIGN_J, DESIGN_M),
    "data_and_analytics": (DATA_J, DATA_M),
    "marketing_and_sales": (SALES_J, SALES_M),
    "management": (MGMT_J, MGMT_M),
    "hr_and_recruitment": (HR_J, HR_M),
    "finance_and_accounting": (FIN_J, FIN_M),
}

SCENARIO_TEMPLATES = {}
for cat_id, (j, m) in CATEGORY_MAP.items():
    SCENARIO_TEMPLATES[cat_id] = {
        "junior": [{"q": x["q"], "options": x["o"]} for x in j],
        "middle": [{"q": x["q"], "options": x["o"]} for x in m],
    }
SCENARIO_TEMPLATES["default"] = {
    "junior": [{"q": x["q"], "options": x["o"]} for x in DEFAULT_J],
    "middle": [{"q": x["q"], "options": x["o"]} for x in DEFAULT_M],
}

