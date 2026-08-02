Interfaces de programmation
===========================

Le projet ne fournit pas d'API REST ou JSON. Son interface HTTP est constituée
de vues Django qui rendent des pages HTML.

Routes HTTP
-----------

============================= ================================ =============
Route                         Vue                              Rôle
============================= ================================ =============
``/``                         ``oc_lettings_site.views.index`` accueil
``/lettings/``                ``lettings.views.index``         locations
``/lettings/<id>/``           ``lettings.views.letting``       détail
``/profiles/``                ``profiles.views.index``         profils
``/profiles/<username>/``     ``profiles.views.profile``       détail
``/admin/``                   administration Django            gestion
``/trigger-500-error/``       test d'exception                  diagnostic
============================= ================================ =============

La route ``/trigger-500-error/`` lève volontairement une exception. Elle sert
uniquement à contrôler la page 500, les journaux et la remontée Sentry.

Référence Python
----------------

Vues principales
~~~~~~~~~~~~~~~~

.. automodule:: oc_lettings_site.views
   :members:

Locations
~~~~~~~~~

.. automodule:: lettings.models
   :members:

.. automodule:: lettings.views
   :members:

Profils
~~~~~~~

.. automodule:: profiles.models
   :members:

.. automodule:: profiles.views
   :members:
