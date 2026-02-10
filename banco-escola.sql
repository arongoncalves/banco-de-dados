-- Tabela de alunos
CREATE TABLE alunos (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_nascimento DATE,
    email TEXT,
    telefone TEXT
);

-- Tabela de professores
CREATE TABLE professores (
    id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT,
    especialidade TEXT
);

-- Tabela de disciplinas
CREATE TABLE disciplinas (
    id_disciplina INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    carga_horaria INTEGER
);

-- Tabela de turmas
CREATE TABLE turmas (
    id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
    id_disciplina INTEGER,
    id_professor INTEGER,
    ano INTEGER,
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina),
    FOREIGN KEY (id_professor) REFERENCES professores(id_professor)
);

-- Tabela de matrículas
CREATE TABLE matriculas (
    id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
    id_aluno INTEGER,
    id_turma INTEGER,
    data_matricula DATE,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma)
);
