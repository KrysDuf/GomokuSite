
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
        string player1;
        string player2;

        public Match(string player1, string player2)
        {
            this.player1 = player1;
            this.player2 = player2;
        }
        public List<string> Play(out string result)
        {
           
            var psi = new ProcessStartInfo();
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
                    process.Close();
                    return intMoveList;
                }
            }
        }
    }
}