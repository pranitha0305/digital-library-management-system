CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    published_year INTEGER
);

public class Book {
    private int id;
    private String title;
    private String author;
    private String genre;
    private int publishedYear;

    // Getters and Setters
}

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class BookDAO {
    private Connection connect() {
        // SQLite connection string
        String url = "jdbc:sqlite:library.db";
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(url);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
        return conn;
    }

    public void insertBook(Book book) {
        String sql = "INSERT INTO books(title, author, genre, published_year) VALUES(?,?,?,?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, book.getTitle());
            pstmt.setString(2, book.getAuthor());
            pstmt.setString(3, book.getGenre());
            pstmt.setInt(4, book.getPublishedYear());
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public List<Book> getAllBooks() {
        String sql = "SELECT id, title, author, genre, published_year FROM books";
        List<Book> books = new ArrayList<>();
        try (Connection conn = this.connect();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                Book book = new Book();
                book.setId(rs.getInt("id"));
                book.setTitle(rs.getString("title"));
                book.setAuthor(rs.getString("author"));
                book.setGenre(rs.getString("genre"));
                book.setPublishedYear(rs.getInt("published_year"));
                books.add(book);
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
        return books;
    }
    
    // Additional CRUD methods (update, delete, find by id) can be added similarly
}

import java.util.List;

public class LibraryService {
    private BookDAO bookDAO;

    public LibraryService() {
        this.bookDAO = new BookDAO();
    }

    public void addBook(Book book) {
        bookDAO.insertBook(book);
    }

    public List<Book> listAllBooks() {
        return bookDAO.getAllBooks();
    }

    // Additional service methods for updating, deleting, and finding books can be added similarly
}

import java.util.List;
import java.util.Scanner;

public class LibraryManagementSystem {
    private static LibraryService libraryService = new LibraryService();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("1. Add Book");
            System.out.println("2. List All Books");
            System.out.println("3. Exit");
            System.out.print("Choose an option: ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // consume newline

            switch (choice) {
                case 1:
                    addBook(scanner);
                    break;
                case 2:
                    listAllBooks();
                    break;
                case 3:
                    System.exit(0);
                default:
                    System.out.println("Invalid option. Please try again.");
            }
        }
    }

    private static void addBook(Scanner scanner) {
        System.out.print("Enter title: ");
        String title = scanner.nextLine();
        System.out.print("Enter author: ");
        String author = scanner.nextLine();
        System.out.print("Enter genre: ");
        String genre = scanner.nextLine();
        System.out.print("Enter published year: ");
        int year = scanner.nextInt();

        Book book = new Book();
        book.setTitle(title);
        book.setAuthor(author);
        book.setGenre(genre);
        book.setPublishedYear(year);

        libraryService.addBook(book);
        System.out.println("Book added successfully.");
    }

    private static void listAllBooks() {
        List<Book> books = libraryService.listAllBooks();
        for (Book book : books) {
            System.out.println("ID: " + book.getId());
            System.out.println("Title: " + book.getTitle());
            System.out.println("Author: " + book.getAuthor());
            System.out.println("Genre: " + book.getGenre());
            System.out.println("Published Year: " + book.getPublishedYear());
            System.out.println();
        }
    }
}

