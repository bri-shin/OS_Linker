import java.io.*;
import java.util.Scanner;
import java.util.ArrayList;

/**
 *
 * @author Jarred van de Voort
 */

public class Linker {
	
	public static void main(String[] args) throws FileNotFoundException {
		
		File fileName = new File(args[0]);
		Scanner scan = new Scanner(fileName);
		
		//Variables to keep track and manipulate components of input file
		int num_mods = scan.nextInt(); 		
		int num_defs = 0;
	    int num_uses = 0;
	    int base_address = 0; 
	    int mod_size = 0;
	    String symbol = null;
	    int sym_loc = 0;
	    int sym_address = 0;
	    String cur_sym = null;
	    int cur_num = 0;
	    int cur_add, new_add = 0;
	    int final_digit = 0;
	    
	    //List of symbols that helps check for duplicates
	    ArrayList<String> symbols = new ArrayList<String>();
	    //List of symbols that are used, used for error checking
	    ArrayList<String> used_symbols = new ArrayList<String>();
	    //List of used uses used for error checking. Say that 3 times fast.
	    ArrayList<String> used_uses = new ArrayList<String>();
	    //List of Addresses
	    ArrayList<String> addresses = new ArrayList<String>();
	    //List of Module sizes
	    ArrayList<Integer> modules = new ArrayList<Integer>();
	    
		System.out.println("Symbol table");
        
		for (int i = 0; i < num_mods; i++){
			num_defs = scan.nextInt();
			
			for (int j = 0; j < num_defs; j++){
				symbol = scan.next();
				
				// Checks for a symbol that is defined more than once
				if(symbols.contains(symbol)){
					System.out.println("Oops! This symbol is defined more than once!");
					
				} else {
					//Calculates absolute address (base address + relative address)
					sym_loc = scan.nextInt();
					sym_address = base_address + sym_loc;
					symbols.add(symbol);
					addresses.add(String.valueOf(sym_address));
					System.out.println(symbol + " = " + sym_address);
					
				}
			}
			
			//Skips over uses, since we don't need this on the first pass
			num_uses = scan.nextInt();
			
			for (int k = 0; k < num_uses; k++){
					scan.next(); //Since the use list is composed of two parts (sym, R_add), we have to skip over both
					scan.next();
			}
			//A running total of the module sizes is kept and sizes are stored to help calculate the absolute address
			mod_size = scan.nextInt();
			base_address += mod_size;
			modules.add(mod_size);
			for (int j = 0; j < mod_size; j++){
					scan.nextInt();
				}
			
        }
		scan.close();
		//End of first pass
		
		//Start of second pass
		System.out.println();
		System.out.println("Memory Map");
		
		base_address = 0; //Fresh set of variables for second pass
		int sym_index = 0;
		int count = -1;
		
		Scanner scan2 = new Scanner(fileName);
		scan2.nextInt(); //Skips # of mods
	
		//A little bit of housekeeping. Here we don't need the definitions but uses instead
		for (int i = 0; i < num_mods; i++){
  			num_defs = scan2.nextInt();
  		
				for (int j = 0; j < num_defs; j++){
					scan2.next();
					scan2.nextInt();
				}
			
				num_uses = scan2.nextInt();
				
				ArrayList<String> uses = new ArrayList<String>();
				for (int k = 0; k < num_uses; k++){
					String next_sym = scan2.next(); 
					uses.add(next_sym);
					used_symbols.add(next_sym);
				}
				
				scan2.next();
				mod_size = scan2.nextInt();
				
				for (int l = 0; l < mod_size; l++){
					count += 1;
					sym_address = -1;
					cur_num = scan2.nextInt();
					final_digit = cur_num % 10; //Gets last digit of current address
					cur_add = (cur_num - final_digit)/10; //Calculates current address
					int base_size = (cur_add/1000)*1000; //Rounds down to nearest 1000
					int total_size = cur_add - base_size;
					
					//Parses the last digit of each number & adjusts address accordingly
					switch(final_digit){
						case 1: //An immediate operand, which is unchanged
							new_add = cur_add;
							break;
						
						case 2: //An absolute address, which is unchanged
							new_add = cur_add;
							if (total_size > 200){ //Error check for machine size (200)
								System.out.println("Oops! Absolute address exceeds machine size");
								new_add = base_size;
							}
							break;
						
						case 3: //A relative address, which is relocated
							new_add = cur_add + base_address;
							if (total_size > mod_size){ //Error check for rel add > mod size
								System.out.printf("Oops! Relative address exceeds module size");
								new_add = base_size;
							}
							break;
						
						//Had trouble with this last case, especially with handling the sentinel 777's and calculating the final address
						case 4: //An external address, which is resolved
							sym_index = cur_add % 10;
							
							if (sym_index == 7) sym_index = 0; //Sentintel intruction. Wasn't too sure how to handle sentinel instr.
							
							if (sym_index >= uses.size()){ //Checks against total number of uses
								new_add = cur_add + base_address;
	  							break;
	  						}						
							
							cur_sym = uses.get(sym_index);
							used_uses.add(cur_sym);
							
							if (!symbols.contains(cur_sym)){ //Checks if current symbol is defined
  								sym_address = 0;
  							} else {
  								sym_address = Integer.valueOf(addresses.get(symbols.indexOf(cur_sym))); 
  							}					
							new_add = cur_add + sym_address - sym_index;//Calculating final address
					}
					
					System.out.println(count + ": " + new_add);
				}
				base_address += mod_size;
		}
		//Checks for uses that are used but not defined
		for (int i = 0; i < used_symbols.size(); i++){
			if(!used_uses.contains(used_symbols.get(i))){
				System.out.println("Oops!" + used_symbols.get(i) + " was used but never defined!");
				}
			}
		
		//Checks for symbols that are defined but never used
		for (int i = 0; i < symbols.size(); i++){
			if(!used_symbols.contains(symbols.get(i))){
				System.out.println("Oops!" + symbols.get(i) + " was defined but never used!");
			}
		}
		
		scan2.close();
	}
	
		
}