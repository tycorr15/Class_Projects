
/*
 * Palindrome.java
 */
   
public class Palindrome {
	public static boolean isPal(String S) {
		Stack<Character> stack1 = new LLStack<Character>();    //the logic is to push the original string on to a stack and a queue
		Stack<Character> stack2 = new LLStack<Character>();		//this allows for comparison of the string. one in orginal order, one reverse
		Queue<Character> queue = new LLQueue<Character>();
		for (int i = 0; i < S.length(); i ++) {
			char j = Character.toUpperCase(S.charAt(i));
			if (j >= 'A' && j <= 'Z') {       				//checking to ensure the value is between A and Z, knowing it's been capitalized.
				stack2.push(j);
				queue.insert(j);
				stack1.pop();								//if it is a letter, add to the stack and queue for comparison
			}
			else {
				stack1.pop();         //if the value isnt a letter, simply remove
			}
		}
		while (stack2.isEmpty() == false || queue.isEmpty() == false) {
			if (stack2.peek() == queue.peek()) {							//peek to compare the values;
				stack2.pop();												//as long as they match, move forward. if different, we know it's false
				queue.remove();
			}
			else {
				return false;
			}
		}
		
		return true;
		
	}
    
    public static void main(String[] args) {
        System.out.println("--- Testing method isPal ---");
        System.out.println();

        System.out.println("(0) Testing on \"A man, a plan, a canal, Panama!\"");
        try {
            boolean results = isPal("A man, a plan, a canal, Panama!");
            System.out.println("actual results:");
            System.out.println(results);
            System.out.println("expected results:");
            System.out.println("true");
            System.out.print("MATCHES EXPECTED RESULTS?: ");
            System.out.println(results == true);
        } catch (Exception e) {
            System.out.println("INCORRECTLY THREW AN EXCEPTION: " + e);
        }
        
        System.out.println();    // include a blank line between tests
        
        /*
         * Add five more unit tests that test a variety of different
         * cases. Follow the same format that we have used above.
         */
        
        System.out.println("(0) Testing on \"Not A Palindrome!\"");
        try {
            boolean results = isPal("Not A Palindrome!");
            System.out.println("actual results:");
            System.out.println(results);
            System.out.println("expected results:");
            System.out.println("false");
            System.out.print("MATCHES EXPECTED RESULTS?: ");
            System.out.println(results == false);
        } catch (Exception e) {
            System.out.println("INCORRECTLY THREW AN EXCEPTION: " + e);
        }
        
        System.out.println();
        
        System.out.println("(0) Testing on \"Unit Tests are SO FUN\"");
        try {
            boolean results = isPal("Unit Tests are SO FUN");
            System.out.println("actual results:");
            System.out.println(results);
            System.out.println("expected results:");
            System.out.println("false");
            System.out.print("MATCHES EXPECTED RESULTS?: ");
            System.out.println(results == false);
        } catch (Exception e) {
            System.out.println("INCORRECTLY THREW AN EXCEPTION: " + e);
        }
        
        System.out.println();
        
        
        System.out.println("(0) Testing on \"TACO# @Cat");
        try {
            boolean results = isPal("TACO# @Cat");
            System.out.println("actual results:");
            System.out.println(results);
            System.out.println("expected results:");
            System.out.println("true");
            System.out.print("MATCHES EXPECTED RESULTS?: ");
            System.out.println(results == true);
        } catch (Exception e) {
            System.out.println("INCORRECTLY THREW AN EXCEPTION: " + e);
        }
        
        System.out.println();
        
        
        
        System.out.println("(0) Testing on \"123456789ono*&%#$%^&*^$#$###");
        try {
            boolean results = isPal("123456789ONO*&%#$%^&*^$#$###");
            System.out.println("actual results:");
            System.out.println(results);
            System.out.println("expected results:");
            System.out.println("true");
            System.out.print("MATCHES EXPECTED RESULTS?: ");
            System.out.println(results == true);
        } catch (Exception e) {
            System.out.println("INCORRECTLY THREW AN EXCEPTION: " + e);
        }
        
        System.out.println();
        
        
        
        
        
        
        
        
        
        
    }
}