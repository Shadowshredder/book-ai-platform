from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from transformers import pipeline

# 🔥 Load models (only once)
summarizer = pipeline("summarization")
qa_model = pipeline("question-answering")


# ✅ GET ALL BOOKS
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# ✅ GET SINGLE BOOK
@api_view(['GET'])
def get_book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    serializer = BookSerializer(book)
    return Response(serializer.data)


# ✅ ADD BOOK
@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)


# ✅ AI SUMMARY
@api_view(['GET'])
def get_summary(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    summary = summarizer(
        book.description,
        max_length=50,
        min_length=20,
        do_sample=False
    )

    return Response({
        "title": book.title,
        "summary": summary[0]['summary_text']
    })


# ✅ AI QUESTION ANSWERING (RAG STYLE 🔥)
@api_view(['POST'])
def ask_question(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    question = request.data.get("question")

    if not question:
        return Response({"error": "Question is required"}, status=400)

    result = qa_model(
        question=question,
        context=book.description
    )

    return Response({
        "book": book.title,
        "question": question,
        "answer": result['answer']
    })