import java.util.Scanner;

public class MarksCalculation {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        int totalMarks[] = new int[5];
        int marks, student;

        for (student = 0; student < 5; student++) {
            totalMarks[student] = 0;
            for (int subject = 0; subject < 5; subject++) {
                System.out.print("Enter marks for student " + (student + 1) + ", subject " + (subject + 1) + ": ");
                marks = scanner.nextInt();
                totalMarks[student] += marks;
            }
        }

        System.out.println("\nTotal Marks:");
        for (student = 0; student < 5; student++) {
            System.out.println("Student " + (student + 1) + ": " + totalMarks[student]);
        }

        System.out.println("\nAverage Marks:");
        for (student = 0; student < 5; student++) {
            System.out.println("Student " + (student + 1) + ": " + (totalMarks[student] / 5.0));
        }

        scanner.close();
    }
}