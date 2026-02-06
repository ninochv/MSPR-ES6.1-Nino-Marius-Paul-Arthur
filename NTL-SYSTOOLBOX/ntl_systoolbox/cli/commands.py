"""
Gestionnaire de commandes CLI pour NTL-SysToolbox.
Exécute les commandes non-interactives.
"""

import sys
from typing import Any
from argparse import Namespace

from ..core import Config, OutputFormatter, ExitCode, get_logger
from ..diagnostic import ServiceChecker, DatabaseChecker, SystemInfoCollector
from ..backup import WMSBackupManager, IntegrityChecker
from ..audit import NetworkScanner, EOLDatabase, ObsolescenceReport


class CommandHandler:
    """
    Gère l'exécution des commandes CLI.
    """
    
    def __init__(self, config: Config = None, output: OutputFormatter = None):
        """
        Initialise le gestionnaire de commandes.
        
        Args:
            config: Instance de configuration
            output: Formateur de sortie
        """
        self.config = config or Config()
        self.output = output or OutputFormatter()
        self.logger = get_logger()
    
    def execute(self, args: Namespace) -> int:
        """
        Exécute une commande basée sur les arguments.
        
        Args:
            args: Arguments parsés
            
        Returns:
            Code de sortie
        """
        command = args.command
        
        if command in ('diagnostic', 'diag'):
            return self._handle_diagnostic(args)
        elif command in ('backup', 'bkp'):
            return self._handle_backup(args)
        elif command == 'audit':
            return self._handle_audit(args)
        else:
            print(f"Commande inconnue: {command}")
            print("Utilisez --help pour voir les commandes disponibles.")
            return ExitCode.UNKNOWN
      
    def _handle_backup(self, args: Namespace) -> int:
        """Gère les commandes du module backup."""
        sub_command = args.backup_command
        
        if sub_command == 'full':
            self.output.set_module("Sauvegarde Complète")
            manager = WMSBackupManager(config=self.config, output=self.output)
            
            output_path = getattr(args, 'output', None)
            manager.backup_full_database(output_path)
            
            return self.output.print_summary()
        
        elif sub_command == 'table':
            self.output.set_module("Export Table CSV")
            manager = WMSBackupManager(config=self.config, output=self.output)
            
            manager.export_table_to_csv(
                args.table_name,
                output_path=getattr(args, 'output', None),
                where_clause=getattr(args, 'where', None)
            )
            
            return self.output.print_summary()
        
        elif sub_command == 'critical':
            self.output.set_module("Sauvegarde Tables Critiques")
            manager = WMSBackupManager(config=self.config, output=self.output)
            manager.backup_critical_tables()
            
            return self.output.print_summary()
        
        elif sub_command == 'verify':
            self.output.set_module("Vérification Intégrité")
            checker = IntegrityChecker(config=self.config, output=self.output)
            
            if getattr(args, 'all', False):
                checker.verify_all_backups()
            elif args.backup_file:
                checker.verify_backup(args.backup_file)
            else:
                checker.verify_all_backups()
            
            return self.output.print_summary()
        
        elif sub_command == 'cleanup':
            self.output.set_module("Nettoyage Sauvegardes")
            manager = WMSBackupManager(config=self.config, output=self.output)
            manager.cleanup_old_backups()
            
            return self.output.print_summary()
        
        else:
            print("Sous-commande backup requise. Utilisez --help.")
            return ExitCode.UNKNOWN
    
