"""Modelos SQLAlchemy para o sistema juridico."""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default="Ativa")  # "Ativa" / "Encerrada"
    peticoes = Column(Integer, default=0)
    tipos = Column(Integer, default=0)
    sintese = Column(Text, default="")
    folder_path = Column(String(1024), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    conversations = relationship("Conversation", back_populates="client")
    documents = relationship("Document", back_populates="client")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    title = Column(String(255), default="Nova conversa")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    client = relationship("Client", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation",
                            order_by="Message.created_at")
    documents = relationship("Document", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # "user" / "assistant" / "system"
    message_type = Column(String(30), default="text")  # "text", "document_preview", "form_input", "status", "checklist", "document_link"
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    conversation = relationship("Conversation", back_populates="messages")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    titulo = Column(String(255), nullable=False)
    file_path = Column(String(1024), nullable=True)
    file_name = Column(String(512), nullable=True)
    status = Column(String(20), default="draft")  # "draft" / "generating" / "completed" / "error"
    content_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    client = relationship("Client", back_populates="documents")
    conversation = relationship("Conversation", back_populates="documents")
