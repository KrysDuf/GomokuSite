
using System.Diagnostics;
using System;
using System.Collections.Generic;  
using System.IO;  
using System.Linq;
using System.Web;
using System.Web.Mvc;


namespace GomukuWebsite.Python
{
    public class HumanMatch
    {
        string AI;
        Process process;

        //AI: ID of the AI
        //process: The Process that is running the game simulation
        public HumanMatch(string AI)
        {
            this.AI = AI;
        }

        //Creates the Process for running the match
        public void Make()
        { 
            var psi = new ProcessStartInfo();
            //Path to python installation change if needed
            psi.FileName = @"C:\Users\Kryst\AppData\Local\Programs\Python\Python39\python.exe";

            var script = HttpContext.Current.Server.MapPath(@"~\Python\gomokuHuman.py");

            psi.Arguments = $"{script} Human {AI}";
            psi.UseShellExecute = false;
            psi.CreateNoWindow = false;
            psi.RedirectStandardInput = true;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;
            process = Process.Start(psi);
        }

        //Return: A string of the AI's move or game result
        public string Read()
        {   
            List<string> intMoveList = new List<string>();
            for (int i = 0; i < 2; i++)
            {
                //reads the lates moves and reformats the string
                string result = process.StandardOutput.ReadLine();
                result = (result.Replace(" ", ""));
                intMoveList.Add(result.Replace("\n", "").Replace("\r", ""));
            }
            return intMoveList[1];
            
        }
        //x: the x coordinate of the human's move
        //y: the y coordinate of the human's move
        public void HumanMove(string x, string y)
        {
            var streamWriter = process.StandardInput;
            streamWriter.WriteLine(x);
            streamWriter.WriteLine(y);
        }

        //Stops the process
        public void End()
        {
            process.Close();
        }
    }
}