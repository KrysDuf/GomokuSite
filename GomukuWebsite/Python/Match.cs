
using System.Diagnostics;
using System;
using System.Collections.Generic;  
using System.IO;  
using System.Linq;
using System.Web;
using System.Web.Mvc;


namespace GomukuWebsite.Python
{
    public class Match
    {
        //player1: ID of the first AI
        //player2: ID of the second AI
        string player1;
        string player2;

        public Match(string player1, string player2)
        {
            this.player1 = player1;
            this.player2 = player2;
        }

        //Creates the Process for running the match
        //Result: A string passed out that has the result message.
        //Return: A List of strings containing each move in order
        public List<string> Play(out string result)
        {
           
            var psi = new ProcessStartInfo();
            //Path to python installation change if needed
            psi.FileName = @"C:\Users\Kryst\AppData\Local\Programs\Python\Python39\python.exe";

            var script = HttpContext.Current.Server.MapPath(@"~\Python\gomoku.py");

            psi.Arguments = $"{script} {player2} {player1}";
            psi.UseShellExecute = false;
            psi.CreateNoWindow = false;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;

            using (Process process = Process.Start(psi))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    //reads the all the moves and reformats the string into an List of strings
                    var game = reader.ReadToEnd();
                    game = (game.Replace(" ", ""));
                    string[] moveList = (game.Replace("\n", "")).Split('\r');
                    List<string> intMoveList = new List<string>();
                    for (int i = 0; i < moveList.Length - 1; i++)
                    {
                        string s = moveList[i];
                        intMoveList.Add(s);
                    }
                    result = moveList[moveList.Length-2].Replace("-1", " White").Replace("1", " Black");
                    //Ends simulation
                    process.Close();
                    return intMoveList;
                }
            }
        }
    }
}